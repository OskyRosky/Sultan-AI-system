"""Manifest-bound Stage 03 feature snapshot loader for 06B.

The loader validates the Stage 03 manifest, then reads only the Parquet files
declared by that manifest. It does not discover files, calculate features,
generate labels, run simulations, compute metrics, or produce evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

import pandas as pd

from loaders.manifest_validator import (
    SnapshotSeriesMetadata,
    SnapshotValidationResult,
    validate_feature_snapshot_manifest,
)


REQUIRED_LINEAGE_COLUMNS = frozenset({"symbol", "timeframe", "timestamp", "run_id"})


@dataclass(frozen=True)
class LoadedFeatureSeries:
    symbol: str
    timeframe: str
    run_id: str
    row_count: int
    min_timestamp: datetime
    max_timestamp: datetime
    parquet_path: Path
    frame: pd.DataFrame


@dataclass(frozen=True)
class LoadedFeatureSnapshot:
    validation_result: SnapshotValidationResult
    manifest_path: Path
    schema_path: Path
    snapshot_id: str
    feature_set: str
    feature_version: str
    code_commit: str
    generated_at: datetime
    source_table: str
    gap_report_reference: str
    quality_report_reference: str
    warmup_policy: str
    series: Mapping[tuple[str, str], LoadedFeatureSeries]


class FeatureSnapshotLoader:
    """Load a validated feature snapshot using only manifest-declared paths."""

    def __init__(
        self,
        manifest_path: str | Path,
        *,
        schema_path: str | Path | None = None,
        repo_root: str | Path | None = None,
    ) -> None:
        self.manifest_path = Path(manifest_path)
        self.repo_root = Path(repo_root) if repo_root is not None else _default_repo_root()
        self.schema_path = (
            Path(schema_path)
            if schema_path is not None
            else self.repo_root
            / "03 Feature Engineering/schemas/feature_snapshot_manifest_schema.json"
        )

    def load(self) -> LoadedFeatureSnapshot:
        validation_result = validate_feature_snapshot_manifest(
            self.manifest_path,
            schema_path=self.schema_path,
        )
        if not validation_result.passed or validation_result.manifest is None:
            raise ValueError(
                "feature snapshot manifest validation failed: "
                + "; ".join(validation_result.errors)
            )

        manifest = validation_result.manifest
        lineage = manifest.lineage
        loaded_series: dict[tuple[str, str], LoadedFeatureSeries] = {}

        for series_metadata in manifest.series:
            key = (series_metadata.symbol, series_metadata.timeframe)
            if key in loaded_series:
                raise ValueError(f"duplicate series key declared: {key}")
            loaded_series[key] = self._load_series(series_metadata)

        return LoadedFeatureSnapshot(
            validation_result=validation_result,
            manifest_path=validation_result.manifest_path,
            schema_path=validation_result.schema_path,
            snapshot_id=lineage.snapshot_id,
            feature_set=lineage.feature_set,
            feature_version=lineage.feature_version,
            code_commit=lineage.code_commit,
            generated_at=lineage.generated_at,
            source_table=lineage.source_table,
            gap_report_reference=lineage.gap_report_reference,
            quality_report_reference=lineage.quality_report_reference,
            warmup_policy=lineage.warmup_policy,
            series=MappingProxyType(loaded_series),
        )

    def _load_series(self, series_metadata: SnapshotSeriesMetadata) -> LoadedFeatureSeries:
        if len(series_metadata.parquet_paths) != 1:
            raise ValueError("each series must declare exactly one parquet path")

        declared_path = Path(series_metadata.parquet_paths[0])
        absolute_path = self._resolve_declared_parquet_path(declared_path)
        frame = pd.read_parquet(absolute_path)
        _validate_required_columns(frame, absolute_path)
        _validate_loaded_lineage(frame, series_metadata, absolute_path)

        if len(frame) != series_metadata.row_count:
            raise ValueError(
                f"loaded row count mismatch for "
                f"{series_metadata.symbol}/{series_metadata.timeframe}: "
                f"manifest={series_metadata.row_count} loaded={len(frame)}"
            )

        return LoadedFeatureSeries(
            symbol=series_metadata.symbol,
            timeframe=series_metadata.timeframe,
            run_id=series_metadata.run_id,
            row_count=len(frame),
            min_timestamp=series_metadata.min_timestamp,
            max_timestamp=series_metadata.max_timestamp,
            parquet_path=absolute_path,
            frame=frame,
        )

    def _resolve_declared_parquet_path(self, declared_path: Path) -> Path:
        if declared_path.is_absolute():
            raise ValueError("parquet paths must be repository-relative")
        if any("_quarantine" in part for part in declared_path.parts):
            raise ValueError("parquet paths must not reference _quarantine")
        if declared_path.suffix != ".parquet":
            raise ValueError("parquet paths must end with .parquet")

        absolute_path = (self.repo_root / declared_path).resolve()
        repo_root = self.repo_root.resolve()
        try:
            absolute_path.relative_to(repo_root)
        except ValueError as exc:
            raise ValueError("parquet paths must remain within repository root") from exc
        if not absolute_path.exists():
            raise FileNotFoundError(f"declared parquet file does not exist: {declared_path}")
        return absolute_path


def _validate_required_columns(frame: pd.DataFrame, parquet_path: Path) -> None:
    missing_columns = REQUIRED_LINEAGE_COLUMNS.difference(frame.columns)
    if missing_columns:
        raise ValueError(
            f"{parquet_path} missing required lineage columns: {sorted(missing_columns)}"
        )


def _validate_loaded_lineage(
    frame: pd.DataFrame,
    series_metadata: SnapshotSeriesMetadata,
    parquet_path: Path,
) -> None:
    _require_single_value(
        frame,
        "symbol",
        series_metadata.symbol,
        series_metadata,
        parquet_path,
    )
    _require_single_value(
        frame,
        "timeframe",
        series_metadata.timeframe,
        series_metadata,
        parquet_path,
    )
    _require_single_value(
        frame,
        "run_id",
        series_metadata.run_id,
        series_metadata,
        parquet_path,
    )


def _require_single_value(
    frame: pd.DataFrame,
    column: str,
    expected_value: str,
    series_metadata: SnapshotSeriesMetadata,
    parquet_path: Path,
) -> None:
    values = set(frame[column].dropna().astype(str).unique())
    if values != {expected_value}:
        raise ValueError(
            f"{parquet_path} {column} mismatch for "
            f"{series_metadata.symbol}/{series_metadata.timeframe}: "
            f"expected={expected_value} loaded={sorted(values)}"
        )


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]
