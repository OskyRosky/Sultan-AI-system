"""Temporal admissibility metadata validator for 06B.

This validator certifies only whether an adapted strategy package has
internally consistent package metadata for later empirical execution. It does
not certify feature formulas, signal timing, execution timing, anti-leakage
correctness, or StrategyDossier temporal semantics. It does not load Parquet
files, discover data, compute returns, create labels, run simulations, perform
OOS or walk-forward validation, compute robustness, score confidence, or
generate evidence.

The official Stage 05 StrategyDossier currently does not expose explicit
required_feature_set, required_symbols, required_timeframes, strategy-specific
temporal windows, strategy-specific feature availability requirements, or
strategy-level decision/execution timing rules. Block 06 therefore certifies
only package_metadata_only consistency.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

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
    strategy_name: str
    strategy_version: str
    certification_scope: str
    certification_status: TemporalAdmissibilityStatus
    certification_reason: str
    handoff_required: bool
    handoff_target: str
    temporal_risks: tuple[str, ...]
    warnings: tuple[str, ...]
    blocking_failures: tuple[str, ...]
    snapshot_id: str
    feature_version: str
    code_commit: str
    generated_at: datetime | None
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
            "strategy_name": self.strategy_name,
            "strategy_version": self.strategy_version,
            "certification_scope": self.certification_scope,
            "certification_status": self.certification_status.value,
            "certification_reason": self.certification_reason,
            "handoff_required": self.handoff_required,
            "handoff_target": self.handoff_target,
            "temporal_risks": list(self.temporal_risks),
            "warnings": list(self.warnings),
            "blocking_failures": list(self.blocking_failures),
            "snapshot_id": self.snapshot_id,
            "feature_version": self.feature_version,
            "code_commit": self.code_commit,
            "generated_at": (
                self.generated_at.isoformat() if self.generated_at is not None else None
            ),
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
        self.validation_timestamp = validation_timestamp or datetime(
            1970,
            1,
            1,
            tzinfo=timezone.utc,
        )

    def validate(self) -> TemporalAdmissibilityResult:
        package = self.adapted_package
        missing: list[str] = []
        failures: list[str] = []
        warnings: list[str] = []

        _require_text(package.adapted_package_id, "package_id", missing)
        _require_text(package.strategy_id, "strategy_id", missing)
        _require_text(package.strategy_name, "strategy_name", missing)
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
        generated_at = _normalize_datetime(package.generated_at, "generated_at", missing)
        validation_timestamp = _normalize_datetime(
            self.validation_timestamp,
            "validation_timestamp",
            missing,
        )

        warnings.append(
            "Stage 05 StrategyDossier does not expose explicit required_feature_set, "
            "required_symbols, required_timeframes, strategy-specific temporal windows, "
            "strategy-specific feature availability requirements, or strategy-level "
            "decision/execution timing rules; Block 06 certifies package metadata only."
        )
        if generated_at is not None and validation_timestamp is not None:
            if generated_at > validation_timestamp:
                failures.append(
                    "generated_at must not be in the future relative to validation_timestamp"
                )

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
            "Package metadata is internally consistent. This does not certify feature "
            "formulas, signal timing, execution timing, anti-leakage correctness, or "
            "StrategyDossier temporal semantics.",
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
        strategy_name=package.strategy_name,
        strategy_version=package.strategy_version,
        certification_scope="package_metadata_only",
        certification_status=status,
        certification_reason=reason,
        handoff_required=True,
        handoff_target="Block 07",
        temporal_risks=temporal_risks,
        warnings=warnings,
        blocking_failures=blocking_failures,
        snapshot_id=package.snapshot_id,
        feature_version=package.feature_version,
        code_commit=package.code_commit,
        generated_at=package.generated_at,
        manifest_path=package.manifest_path,
        schema_path=package.schema_path,
    )


def _require_text(value: object, field_name: str, missing: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        missing.append(f"{field_name} must be present")


def _require_path(value: object, field_name: str, missing: list[str]) -> None:
    if not isinstance(value, Path) or not str(value).strip() or not value.is_file():
        missing.append(f"{field_name} must reference an existing file")


def _normalize_datetime(
    value: object,
    field_name: str,
    missing: list[str],
) -> datetime | None:
    if value is None:
        missing.append(f"{field_name} must be present")
        return None
    if not isinstance(value, datetime):
        missing.append(f"{field_name} must be a datetime")
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value
