"""Stage 03 feature snapshot manifest validation for 06B.

This module validates manifest structure and declared metadata only. It does
not load Parquet files, query PostgreSQL, run backtests, or generate evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
from typing import Any, Mapping

from jsonschema import Draft202012Validator


SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


@dataclass(frozen=True)
class SnapshotSeriesMetadata:
    exchange: str
    symbol: str
    timeframe: str
    run_id: str
    min_timestamp: datetime
    max_timestamp: datetime
    row_count: int
    data_quality_score: float
    parquet_paths: tuple[str, ...]


@dataclass(frozen=True)
class SnapshotLineageMetadata:
    snapshot_id: str
    generated_at: datetime
    feature_set: str
    feature_version: str
    source_table: str
    status: str
    ready_for_backtesting: bool
    warmup_policy: str
    gap_report_reference: str
    quality_report_reference: str
    code_commit: str
    notes: str


@dataclass(frozen=True)
class FeatureSnapshotManifest:
    lineage: SnapshotLineageMetadata
    symbols: tuple[str, ...]
    timeframes: tuple[str, ...]
    series: tuple[SnapshotSeriesMetadata, ...]


@dataclass(frozen=True)
class SnapshotValidationResult:
    passed: bool
    manifest: FeatureSnapshotManifest | None
    errors: tuple[str, ...]
    manifest_path: Path
    schema_path: Path
    warnings: tuple[str, ...] = ()


def validate_feature_snapshot_manifest(
    manifest_path: str | Path,
    *,
    schema_path: str | Path,
) -> SnapshotValidationResult:
    """Validate a Stage 03 feature snapshot manifest against schema and 06 rules."""

    path = Path(manifest_path)
    schema = _read_json(Path(schema_path))
    payload = _read_json(path)

    errors = _schema_errors(payload, schema)
    if errors:
        return SnapshotValidationResult(
            passed=False,
            manifest=None,
            errors=tuple(errors),
            manifest_path=path,
            schema_path=Path(schema_path),
        )

    try:
        manifest = parse_feature_snapshot_manifest(payload)
        _validate_manifest_metadata(manifest)
    except (TypeError, ValueError) as exc:
        return SnapshotValidationResult(
            passed=False,
            manifest=None,
            errors=(str(exc),),
            manifest_path=path,
            schema_path=Path(schema_path),
        )

    return SnapshotValidationResult(
        passed=True,
        manifest=manifest,
        errors=(),
        manifest_path=path,
        schema_path=Path(schema_path),
    )


def parse_feature_snapshot_manifest(payload: Mapping[str, Any]) -> FeatureSnapshotManifest:
    """Parse an already schema-valid manifest payload into typed immutable models."""

    lineage = SnapshotLineageMetadata(
        snapshot_id=_require_text(payload["snapshot_id"], "snapshot_id"),
        generated_at=_parse_datetime(payload["generated_at"], "generated_at"),
        feature_set=_require_text(payload["feature_set"], "feature_set"),
        feature_version=_require_text(payload["feature_version"], "feature_version"),
        source_table=_require_text(payload["source_table"], "source_table"),
        status=_require_text(payload["status"], "status"),
        ready_for_backtesting=bool(payload["ready_for_backtesting"]),
        warmup_policy=_require_text(payload["warmup_policy"], "warmup_policy"),
        gap_report_reference=_require_text(
            payload["gap_report_reference"],
            "gap_report_reference",
        ),
        quality_report_reference=_require_text(
            payload["quality_report_reference"],
            "quality_report_reference",
        ),
        code_commit=_require_text(payload["code_commit"], "code_commit"),
        notes=_require_text(payload["notes"], "notes"),
    )
    series = tuple(_parse_series(item) for item in payload["series"])
    return FeatureSnapshotManifest(
        lineage=lineage,
        symbols=_normalize_text_sequence(payload["symbols"], "symbols"),
        timeframes=_normalize_text_sequence(payload["timeframes"], "timeframes"),
        series=series,
    )


def _parse_series(payload: Mapping[str, Any]) -> SnapshotSeriesMetadata:
    return SnapshotSeriesMetadata(
        exchange=_require_text(payload["exchange"], "series.exchange"),
        symbol=_require_text(payload["symbol"], "series.symbol"),
        timeframe=_require_text(payload["timeframe"], "series.timeframe"),
        run_id=_require_text(payload["run_id"], "series.run_id"),
        min_timestamp=_parse_datetime(payload["min_timestamp"], "series.min_timestamp"),
        max_timestamp=_parse_datetime(payload["max_timestamp"], "series.max_timestamp"),
        row_count=int(payload["row_count"]),
        data_quality_score=float(payload["data_quality_score"]),
        parquet_paths=_normalize_text_sequence(
            payload["parquet_paths"],
            "series.parquet_paths",
        ),
    )


def _validate_manifest_metadata(manifest: FeatureSnapshotManifest) -> None:
    lineage = manifest.lineage
    if not SEMVER_PATTERN.fullmatch(lineage.feature_version):
        raise ValueError("feature_version must follow SemVer MAJOR.MINOR.PATCH")
    if lineage.status != "complete":
        raise ValueError("manifest status must be complete for 06 consumption")
    if not lineage.ready_for_backtesting:
        raise ValueError("ready_for_backtesting must be true for 06 consumption")
    if not manifest.series:
        raise ValueError("series must contain at least one item")

    declared_pairs = {(series.symbol, series.timeframe) for series in manifest.series}
    expected_pairs = {
        (symbol, timeframe)
        for symbol in manifest.symbols
        for timeframe in manifest.timeframes
    }
    if len(manifest.symbols) != len(set(manifest.symbols)):
        raise ValueError("symbols must not contain duplicates")
    if len(manifest.timeframes) != len(set(manifest.timeframes)):
        raise ValueError("timeframes must not contain duplicates")
    if declared_pairs != expected_pairs:
        raise ValueError("series must cover every declared symbol/timeframe pair exactly")
    if len(manifest.series) != len(declared_pairs):
        raise ValueError("series must not contain duplicate symbol/timeframe pairs")

    for series in manifest.series:
        _validate_series_metadata(series, lineage)


def _validate_series_metadata(
    series: SnapshotSeriesMetadata,
    lineage: SnapshotLineageMetadata,
) -> None:
    if series.min_timestamp > series.max_timestamp:
        raise ValueError("series min_timestamp must be <= max_timestamp")
    if series.row_count <= 0:
        raise ValueError("series row_count must be positive")
    if not 0.0 <= series.data_quality_score <= 1.0:
        raise ValueError("series data_quality_score must be between 0 and 1")
    if not series.parquet_paths:
        raise ValueError("series parquet_paths must contain at least one path")
    for parquet_path in series.parquet_paths:
        _validate_parquet_reference(parquet_path, series, lineage)


def _validate_parquet_reference(
    parquet_path: str,
    series: SnapshotSeriesMetadata,
    lineage: SnapshotLineageMetadata,
) -> None:
    path = Path(parquet_path)
    if path.is_absolute():
        raise ValueError("parquet paths must be repository-relative")
    if path.suffix != ".parquet":
        raise ValueError("parquet paths must end with .parquet")
    expected_parts = (
        lineage.feature_set,
        lineage.feature_version,
        series.symbol,
        series.timeframe,
    )
    missing_parts = [part for part in expected_parts if part not in path.parts]
    if missing_parts:
        raise ValueError(f"parquet path missing expected lineage parts: {missing_parts}")
    if series.run_id not in path.name:
        raise ValueError("parquet filename must include series run_id")


def _schema_errors(payload: Mapping[str, Any], schema: Mapping[str, Any]) -> list[str]:
    validator = Draft202012Validator(schema)
    return [
        f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(payload), key=str)
    ]


def _read_json(path: Path) -> Mapping[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _parse_datetime(value: object, field_name: str) -> datetime:
    text = _require_text(value, field_name)
    normalized = text.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be an ISO datetime") from exc


def _require_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _normalize_text_sequence(values: object, field_name: str) -> tuple[str, ...]:
    if not isinstance(values, list | tuple):
        raise TypeError(f"{field_name} must be a sequence")
    normalized = tuple(_require_text(value, field_name) for value in values)
    if not normalized:
        raise ValueError(f"{field_name} must contain at least one item")
    return normalized
