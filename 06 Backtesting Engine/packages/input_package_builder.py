"""Governed non-empirical input package builder for 06B.

This module binds a loaded Stage 03 feature snapshot into a deterministic
metadata package. It does not load Parquet files, discover files, calculate
signals or labels, run simulations, compute metrics, or generate evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from contracts.motor_b_output_contract import (
    AvailabilityStatus,
    ConfidenceStatus,
    OOSValidationStatus,
    PaperTradingEligibility,
    RobustnessStatus,
    SimulationStatus,
)
from loaders.feature_snapshot_loader import LoadedFeatureSnapshot


@dataclass(frozen=True)
class InputPackageSeriesReference:
    symbol: str
    timeframe: str
    run_id: str
    row_count: int
    min_timestamp: datetime
    max_timestamp: datetime
    parquet_path: Path

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "run_id": self.run_id,
            "row_count": self.row_count,
            "min_timestamp": self.min_timestamp.isoformat(),
            "max_timestamp": self.max_timestamp.isoformat(),
            "parquet_path": str(self.parquet_path),
        }


@dataclass(frozen=True)
class InputPackageLineage:
    snapshot_id: str
    feature_set: str
    feature_version: str
    code_commit: str
    generated_at: datetime
    source_table: str
    manifest_path: Path
    schema_path: Path
    gap_report_reference: str
    quality_report_reference: str
    warmup_policy: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "feature_set": self.feature_set,
            "feature_version": self.feature_version,
            "code_commit": self.code_commit,
            "generated_at": self.generated_at.isoformat(),
            "source_table": self.source_table,
            "manifest_path": str(self.manifest_path),
            "schema_path": str(self.schema_path),
            "gap_report_reference": self.gap_report_reference,
            "quality_report_reference": self.quality_report_reference,
            "warmup_policy": self.warmup_policy,
        }


@dataclass(frozen=True)
class InputPackageGovernanceState:
    strategy_dossier_bound: bool
    strategy_dossier_id: str | None
    temporal_admissibility_status: str
    simulation_status: SimulationStatus
    oos_validation_status: OOSValidationStatus
    walk_forward_status: str
    robustness_status: RobustnessStatus
    empirical_results_available: bool
    confidence_status: ConfidenceStatus
    confidence_score: float | None
    paper_trading_eligibility: PaperTradingEligibility
    stage_09_readiness: str
    handoff_to_09: str

    @classmethod
    def blocked(cls) -> InputPackageGovernanceState:
        return cls(
            strategy_dossier_bound=False,
            strategy_dossier_id=None,
            temporal_admissibility_status=(
                AvailabilityStatus.TEMPORAL_ADMISSIBILITY_NOT_CERTIFIED.value
            ),
            simulation_status=SimulationStatus.BACKTEST_NOT_IMPLEMENTED,
            oos_validation_status=OOSValidationStatus.OOS_NOT_AVAILABLE,
            walk_forward_status=AvailabilityStatus.WALK_FORWARD_NOT_AVAILABLE.value,
            robustness_status=RobustnessStatus.ROBUSTNESS_NOT_AVAILABLE,
            empirical_results_available=False,
            confidence_status=ConfidenceStatus.CONFIDENCE_NOT_AVAILABLE,
            confidence_score=None,
            paper_trading_eligibility=PaperTradingEligibility.BLOCKED,
            stage_09_readiness="blocked",
            handoff_to_09="blocked",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy_dossier_bound": self.strategy_dossier_bound,
            "strategy_dossier_id": self.strategy_dossier_id,
            "temporal_admissibility_status": self.temporal_admissibility_status,
            "simulation_status": self.simulation_status.value,
            "oos_validation_status": self.oos_validation_status.value,
            "walk_forward_status": self.walk_forward_status,
            "robustness_status": self.robustness_status.value,
            "empirical_results_available": self.empirical_results_available,
            "confidence_status": self.confidence_status.value,
            "confidence_score": self.confidence_score,
            "paper_trading_eligibility": self.paper_trading_eligibility.value,
            "stage_09_readiness": self.stage_09_readiness,
            "handoff_to_09": self.handoff_to_09,
        }


@dataclass(frozen=True)
class BacktestInputPackage:
    input_package_id: str
    created_at: datetime
    lineage: InputPackageLineage
    governance_state: InputPackageGovernanceState
    series: Mapping[tuple[str, str], InputPackageSeriesReference]

    @property
    def snapshot_id(self) -> str:
        return self.lineage.snapshot_id

    @property
    def feature_set(self) -> str:
        return self.lineage.feature_set

    @property
    def feature_version(self) -> str:
        return self.lineage.feature_version

    @property
    def code_commit(self) -> str:
        return self.lineage.code_commit

    @property
    def generated_at(self) -> datetime:
        return self.lineage.generated_at

    @property
    def source_table(self) -> str:
        return self.lineage.source_table

    @property
    def manifest_path(self) -> Path:
        return self.lineage.manifest_path

    @property
    def schema_path(self) -> Path:
        return self.lineage.schema_path

    @property
    def gap_report_reference(self) -> str:
        return self.lineage.gap_report_reference

    @property
    def quality_report_reference(self) -> str:
        return self.lineage.quality_report_reference

    @property
    def warmup_policy(self) -> str:
        return self.lineage.warmup_policy

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_package_id": self.input_package_id,
            "created_at": self.created_at.isoformat(),
            "lineage": self.lineage.to_dict(),
            "governance_state": self.governance_state.to_dict(),
            "series": {
                f"{symbol}|{timeframe}": reference.to_dict()
                for (symbol, timeframe), reference in sorted(self.series.items())
            },
        }


class InputPackageBuilder:
    """Build deterministic input packages from already-loaded feature snapshots."""

    def __init__(self, loaded_snapshot: LoadedFeatureSnapshot) -> None:
        self.loaded_snapshot = loaded_snapshot

    def build(self, *, created_at: datetime | None = None) -> BacktestInputPackage:
        series_references = {
            key: InputPackageSeriesReference(
                symbol=series.symbol,
                timeframe=series.timeframe,
                run_id=series.run_id,
                row_count=series.row_count,
                min_timestamp=series.min_timestamp,
                max_timestamp=series.max_timestamp,
                parquet_path=series.parquet_path,
            )
            for key, series in sorted(self.loaded_snapshot.series.items())
        }

        lineage = InputPackageLineage(
            snapshot_id=self.loaded_snapshot.snapshot_id,
            feature_set=self.loaded_snapshot.feature_set,
            feature_version=self.loaded_snapshot.feature_version,
            code_commit=self.loaded_snapshot.code_commit,
            generated_at=self.loaded_snapshot.generated_at,
            source_table=self.loaded_snapshot.source_table,
            manifest_path=self.loaded_snapshot.manifest_path,
            schema_path=self.loaded_snapshot.schema_path,
            gap_report_reference=self.loaded_snapshot.gap_report_reference,
            quality_report_reference=self.loaded_snapshot.quality_report_reference,
            warmup_policy=self.loaded_snapshot.warmup_policy,
        )

        return BacktestInputPackage(
            input_package_id=_deterministic_input_package_id(lineage, series_references),
            created_at=created_at or datetime.now(timezone.utc),
            lineage=lineage,
            governance_state=InputPackageGovernanceState.blocked(),
            series=MappingProxyType(series_references),
        )


def build_backtest_input_package(
    loaded_snapshot: LoadedFeatureSnapshot,
    *,
    created_at: datetime | None = None,
) -> BacktestInputPackage:
    return InputPackageBuilder(loaded_snapshot).build(created_at=created_at)


def _deterministic_input_package_id(
    lineage: InputPackageLineage,
    series_references: Mapping[tuple[str, str], InputPackageSeriesReference],
) -> str:
    payload = {
        "snapshot_id": lineage.snapshot_id,
        "feature_set": lineage.feature_set,
        "feature_version": lineage.feature_version,
        "code_commit": lineage.code_commit,
        "source_table": lineage.source_table,
        "series": [
            {
                "symbol": reference.symbol,
                "timeframe": reference.timeframe,
                "run_id": reference.run_id,
                "row_count": reference.row_count,
                "min_timestamp": reference.min_timestamp.isoformat(),
                "max_timestamp": reference.max_timestamp.isoformat(),
                "parquet_path": str(reference.parquet_path),
            }
            for _, reference in sorted(series_references.items())
        ],
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return f"backtest-input-{digest[:16]}"
