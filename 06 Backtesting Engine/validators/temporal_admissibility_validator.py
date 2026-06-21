"""Temporal admissibility metadata validator for 06B.

This validator certifies only whether an adapted strategy package has enough
consistent temporal metadata for later empirical execution. It does not load
Parquet files, discover data, compute returns, create labels, run simulations,
perform OOS or walk-forward validation, compute robustness, score confidence,
or generate evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import json
from pathlib import Path
from typing import Any, Mapping

from adapters.strategy_dossier_adapter import AdaptedBacktestPackage


class TemporalAdmissibilityStatus(str, Enum):
    CERTIFIED = "certified"
    REJECTED = "rejected"
    INSUFFICIENT_INFORMATION = "insufficient_information"


@dataclass(frozen=True)
class TemporalAdmissibilityResult:
    admissible: bool
    validation_timestamp: datetime
    package_id: str
    strategy_id: str
    strategy_version: str
    certification_status: TemporalAdmissibilityStatus
    certification_reason: str
    temporal_risks: tuple[str, ...]
    warnings: tuple[str, ...]
    blocking_failures: tuple[str, ...]
    snapshot_id: str
    feature_version: str
    code_commit: str
    manifest_path: Path
    schema_path: Path

    def __post_init__(self) -> None:
        if not isinstance(self.certification_status, TemporalAdmissibilityStatus):
            raise TypeError(
                "certification_status must be a TemporalAdmissibilityStatus"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "admissible": self.admissible,
            "validation_timestamp": self.validation_timestamp.isoformat(),
            "package_id": self.package_id,
            "strategy_id": self.strategy_id,
            "strategy_version": self.strategy_version,
            "certification_status": self.certification_status.value,
            "certification_reason": self.certification_reason,
            "temporal_risks": list(self.temporal_risks),
            "warnings": list(self.warnings),
            "blocking_failures": list(self.blocking_failures),
            "snapshot_id": self.snapshot_id,
            "feature_version": self.feature_version,
            "code_commit": self.code_commit,
            "manifest_path": str(self.manifest_path),
            "schema_path": str(self.schema_path),
        }


class TemporalAdmissibilityValidator:
    """Read-only temporal metadata validator for adapted 06B packages."""

    def __init__(
        self,
        adapted_package: AdaptedBacktestPackage,
        *,
        validation_timestamp: datetime | None = None,
    ) -> None:
        self.adapted_package = adapted_package
        self.validation_timestamp = validation_timestamp or datetime(1970, 1, 1, tzinfo=timezone.utc)

    def validate(self) -> TemporalAdmissibilityResult:
        package = self.adapted_package
        missing: list[str] = []
        failures: list[str] = []
        warnings: list[str] = []

        _require_text(package.adapted_package_id, "package_id", missing)
        _require_text(package.strategy_id, "strategy_id", missing)
        _require_text(package.strategy_version, "strategy_version", missing)
        _require_text(package.snapshot_id, "snapshot_id", missing)
        _require_text(package.feature_version, "feature_version", missing)
        _require_text(package.code_commit, "code_commit", missing)
        _require_text(package.feature_set, "feature_set", missing)
        _require_text(package.gap_report_reference, "gap_report_reference", missing)
        _require_text(package.quality_report_reference, "quality_report_reference", missing)
        _require_text(package.warmup_policy, "warmup_policy", missing)
        _require_path(package.manifest_path, "manifest_path", missing)
        _require_path(package.schema_path, "schema_path", missing)

        manifest_payload = _read_manifest_payload(package.manifest_path, missing)
        generated_at = _parse_generated_at(manifest_payload, missing)

        if not package.series:
            missing.append("series must contain at least one item")

        seen_series: set[tuple[str, str]] = set()
        for key, series in package.series.items():
            series_key = (series.symbol, series.timeframe)
            if key != series_key:
                failures.append(
                    f"series key {key} does not match metadata key {series_key}"
                )
            if series_key in seen_series:
                failures.append(f"duplicate symbol/timeframe series: {series_key}")
            seen_series.add(series_key)

            _require_text(series.symbol, "series.symbol", missing)
            _require_text(series.timeframe, "series.timeframe", missing)
            _require_text(series.run_id, "series.run_id", missing)
            _require_path(series.parquet_path, "series.parquet_path", missing)
            if series.row_count <= 0:
                failures.append(
                    f"series {series.symbol}/{series.timeframe} row_count must be positive"
                )
            if series.min_timestamp is None:
                missing.append(f"series {series.symbol}/{series.timeframe} min_timestamp missing")
            if series.max_timestamp is None:
                missing.append(f"series {series.symbol}/{series.timeframe} max_timestamp missing")
            if series.min_timestamp is not None and series.max_timestamp is not None:
                if series.min_timestamp > series.max_timestamp:
                    failures.append(
                        f"series {series.symbol}/{series.timeframe} min_timestamp "
                        "must be <= max_timestamp"
                    )
                if generated_at is not None and series.max_timestamp > generated_at:
                    failures.append(
                        f"series {series.symbol}/{series.timeframe} contains future "
                        "timestamps relative to snapshot generation time"
                    )

        if missing:
            return _result(
                package,
                self.validation_timestamp,
                TemporalAdmissibilityStatus.INSUFFICIENT_INFORMATION,
                "Temporal admissibility cannot be determined because required metadata is missing.",
                temporal_risks=(),
                warnings=tuple(warnings),
                blocking_failures=tuple(dict.fromkeys(missing)),
            )

        if failures:
            return _result(
                package,
                self.validation_timestamp,
                TemporalAdmissibilityStatus.REJECTED,
                "Temporal admissibility rejected due to blocking temporal metadata failures.",
                temporal_risks=tuple(dict.fromkeys(failures)),
                warnings=tuple(warnings),
                blocking_failures=tuple(dict.fromkeys(failures)),
            )

        return _result(
            package,
            self.validation_timestamp,
            TemporalAdmissibilityStatus.CERTIFIED,
            "Temporal admissibility certified from package metadata only.",
            temporal_risks=(),
            warnings=tuple(warnings),
            blocking_failures=(),
        )


def validate_temporal_admissibility(
    adapted_package: AdaptedBacktestPackage,
    *,
    validation_timestamp: datetime | None = None,
) -> TemporalAdmissibilityResult:
    return TemporalAdmissibilityValidator(
        adapted_package,
        validation_timestamp=validation_timestamp,
    ).validate()


def _result(
    package: AdaptedBacktestPackage,
    validation_timestamp: datetime,
    status: TemporalAdmissibilityStatus,
    reason: str,
    *,
    temporal_risks: tuple[str, ...],
    warnings: tuple[str, ...],
    blocking_failures: tuple[str, ...],
) -> TemporalAdmissibilityResult:
    return TemporalAdmissibilityResult(
        admissible=status is TemporalAdmissibilityStatus.CERTIFIED,
        validation_timestamp=validation_timestamp,
        package_id=package.adapted_package_id,
        strategy_id=package.strategy_id,
        strategy_version=package.strategy_version,
        certification_status=status,
        certification_reason=reason,
        temporal_risks=temporal_risks,
        warnings=warnings,
        blocking_failures=blocking_failures,
        snapshot_id=package.snapshot_id,
        feature_version=package.feature_version,
        code_commit=package.code_commit,
        manifest_path=package.manifest_path,
        schema_path=package.schema_path,
    )


def _require_text(value: object, field_name: str, missing: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        missing.append(f"{field_name} must be present")


def _require_path(value: object, field_name: str, missing: list[str]) -> None:
    if not isinstance(value, Path) or not str(value).strip() or not value.is_file():
        missing.append(f"{field_name} must reference an existing file")


def _read_manifest_payload(path: Path, missing: list[str]) -> Mapping[str, Any] | None:
    if not isinstance(path, Path) or not path.is_file():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        missing.append(f"manifest_path must contain readable JSON: {exc}")
        return None
    if not isinstance(payload, dict):
        missing.append("manifest_path must contain a JSON object")
        return None
    return payload


def _parse_generated_at(
    payload: Mapping[str, Any] | None,
    missing: list[str],
) -> datetime | None:
    if payload is None:
        return None
    value = payload.get("generated_at")
    if not isinstance(value, str) or not value.strip():
        missing.append("generated_at must be present")
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        missing.append("generated_at must be an ISO datetime")
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed
