"""Structural StrategyDossier adapter for 06B.

This adapter binds a governed input package to the official conceptual
StrategyDossier contract. It preserves lineage and governance restrictions only;
it does not load data, execute strategy logic, certify temporal admissibility,
simulate trades, compute metrics, or generate evidence.

The official Stage 05 StrategyDossier currently does not expose explicit
required_feature_set, required_symbols, required_timeframes, strategy-specific
temporal windows, strategy-specific feature availability requirements, or
strategy-level decision/execution timing rules. Those limitations are carried
forward so Block 06 can certify only package metadata consistency.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from packages.input_package_builder import BacktestInputPackage


STRATEGY_ENGINE_ROOT = Path(__file__).resolve().parents[2] / "05 Strategy Engine"
if str(STRATEGY_ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from reports.strategy_dossier import StrategyDossier  # noqa: E402


@dataclass(frozen=True)
class AdaptedSeriesReference:
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
class AdaptedGovernanceState:
    strategy_dossier_bound: bool
    strategy_dossier_id: str
    temporal_admissibility_status: str
    simulation_status: str
    oos_validation_status: str
    walk_forward_status: str
    robustness_status: str
    empirical_results_available: bool
    confidence_status: str
    confidence_score: float | None
    paper_trading_eligibility: str
    stage_09_readiness: str
    handoff_to_09: str

    @classmethod
    def from_input_package(
        cls,
        input_package: BacktestInputPackage,
        *,
        strategy_dossier_id: str,
    ) -> AdaptedGovernanceState:
        source = input_package.governance_state
        return cls(
            strategy_dossier_bound=True,
            strategy_dossier_id=strategy_dossier_id,
            temporal_admissibility_status=source.temporal_admissibility_status,
            simulation_status=source.simulation_status.value,
            oos_validation_status=source.oos_validation_status.value,
            walk_forward_status=source.walk_forward_status,
            robustness_status=source.robustness_status.value,
            empirical_results_available=source.empirical_results_available,
            confidence_status=source.confidence_status.value,
            confidence_score=source.confidence_score,
            paper_trading_eligibility=source.paper_trading_eligibility.value,
            stage_09_readiness=source.stage_09_readiness,
            handoff_to_09=source.handoff_to_09,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy_dossier_bound": self.strategy_dossier_bound,
            "strategy_dossier_id": self.strategy_dossier_id,
            "temporal_admissibility_status": self.temporal_admissibility_status,
            "simulation_status": self.simulation_status,
            "oos_validation_status": self.oos_validation_status,
            "walk_forward_status": self.walk_forward_status,
            "robustness_status": self.robustness_status,
            "empirical_results_available": self.empirical_results_available,
            "confidence_status": self.confidence_status,
            "confidence_score": self.confidence_score,
            "paper_trading_eligibility": self.paper_trading_eligibility,
            "stage_09_readiness": self.stage_09_readiness,
            "handoff_to_09": self.handoff_to_09,
        }


@dataclass(frozen=True)
class AdaptedBacktestPackage:
    adapted_package_id: str
    input_package_id: str
    snapshot_id: str
    strategy_id: str
    strategy_name: str
    strategy_version: str
    feature_set: str
    feature_version: str
    code_commit: str
    generated_at: datetime
    manifest_path: Path
    schema_path: Path
    gap_report_reference: str
    quality_report_reference: str
    warmup_policy: str
    series: Mapping[tuple[str, str], AdaptedSeriesReference]
    governance_state: AdaptedGovernanceState

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapted_package_id": self.adapted_package_id,
            "input_package_id": self.input_package_id,
            "snapshot_id": self.snapshot_id,
            "strategy_id": self.strategy_id,
            "strategy_name": self.strategy_name,
            "strategy_version": self.strategy_version,
            "feature_set": self.feature_set,
            "feature_version": self.feature_version,
            "code_commit": self.code_commit,
            "generated_at": self.generated_at.isoformat(),
            "manifest_path": str(self.manifest_path),
            "schema_path": str(self.schema_path),
            "gap_report_reference": self.gap_report_reference,
            "quality_report_reference": self.quality_report_reference,
            "warmup_policy": self.warmup_policy,
            "governance_state": self.governance_state.to_dict(),
            "series": {
                f"{symbol}|{timeframe}": reference.to_dict()
                for (symbol, timeframe), reference in sorted(self.series.items())
            },
        }


class StrategyDossierAdapter:
    """Bind one BacktestInputPackage to one official StrategyDossier."""

    def __init__(
        self,
        input_package: BacktestInputPackage,
        dossier: StrategyDossier | None,
    ) -> None:
        self.input_package = input_package
        self.dossier = dossier

    def adapt(self) -> AdaptedBacktestPackage:
        dossier = _require_strategy_dossier(self.dossier)
        identity = _extract_strategy_identity(dossier)
        _reject_archived_or_deprecated(dossier)
        _validate_feature_compatibility(dossier, self.input_package)
        _validate_series_availability(dossier, self.input_package)

        series = {
            key: AdaptedSeriesReference(
                symbol=reference.symbol,
                timeframe=reference.timeframe,
                run_id=reference.run_id,
                row_count=reference.row_count,
                min_timestamp=reference.min_timestamp,
                max_timestamp=reference.max_timestamp,
                parquet_path=reference.parquet_path,
            )
            for key, reference in sorted(self.input_package.series.items())
        }

        return AdaptedBacktestPackage(
            adapted_package_id=_deterministic_adapted_package_id(
                self.input_package.input_package_id,
                identity["strategy_id"],
                identity["strategy_version"],
            ),
            input_package_id=self.input_package.input_package_id,
            snapshot_id=self.input_package.snapshot_id,
            strategy_id=identity["strategy_id"],
            strategy_name=identity["strategy_name"],
            strategy_version=identity["strategy_version"],
            feature_set=self.input_package.feature_set,
            feature_version=self.input_package.feature_version,
            code_commit=self.input_package.code_commit,
            generated_at=self.input_package.generated_at,
            manifest_path=self.input_package.manifest_path,
            schema_path=self.input_package.schema_path,
            gap_report_reference=self.input_package.gap_report_reference,
            quality_report_reference=self.input_package.quality_report_reference,
            warmup_policy=self.input_package.warmup_policy,
            series=MappingProxyType(series),
            governance_state=AdaptedGovernanceState.from_input_package(
                self.input_package,
                strategy_dossier_id=identity["strategy_id"],
            ),
        )


def adapt_strategy_dossier(
    input_package: BacktestInputPackage,
    dossier: StrategyDossier | None,
) -> AdaptedBacktestPackage:
    return StrategyDossierAdapter(input_package, dossier).adapt()


def _require_strategy_dossier(dossier: StrategyDossier | None) -> StrategyDossier:
    if dossier is None:
        raise ValueError("StrategyDossier is required")
    if not isinstance(dossier, StrategyDossier):
        raise TypeError("dossier must be a StrategyDossier")
    return dossier


def _extract_strategy_identity(dossier: StrategyDossier) -> dict[str, str]:
    closure_record = dossier.closure_record
    strategy_id = _require_text(dossier.dossier_id, "strategy_id")
    strategy_name = _require_text(closure_record.closure_summary, "strategy_name")
    strategy_version = _require_text(closure_record.closure_id, "strategy_version")
    return {
        "strategy_id": strategy_id,
        "strategy_name": strategy_name,
        "strategy_version": strategy_version,
    }


def _reject_archived_or_deprecated(dossier: StrategyDossier) -> None:
    status_values = {
        _normalize_status_value(getattr(dossier, "status", "")),
        _normalize_status_value(getattr(dossier, "lifecycle_status", "")),
        _normalize_status_value(getattr(dossier, "handoff_status", "")),
        _normalize_status_value(getattr(dossier.closure_record, "closure_status", "")),
    }
    if "deprecated" in status_values:
        raise ValueError("StrategyDossier must not be deprecated")
    if "archived" in status_values:
        raise ValueError("StrategyDossier must not be archived")


def _validate_feature_compatibility(
    dossier: StrategyDossier,
    input_package: BacktestInputPackage,
) -> None:
    required_feature_sets = _collect_optional_text_values(
        dossier,
        ("feature_set", "required_feature_set", "feature_sets", "required_feature_sets"),
    )
    if not required_feature_sets:
        return
    if input_package.feature_set not in required_feature_sets:
        raise ValueError(
            "StrategyDossier feature_set requirements do not match input package"
        )


def _validate_series_availability(
    dossier: StrategyDossier,
    input_package: BacktestInputPackage,
) -> None:
    available_symbols = {symbol for symbol, _ in input_package.series}
    available_timeframes = {timeframe for _, timeframe in input_package.series}
    required_symbols = _collect_optional_text_values(
        dossier,
        ("symbol", "symbols", "required_symbol", "required_symbols"),
    )
    required_timeframes = _collect_optional_text_values(
        dossier,
        ("timeframe", "timeframes", "required_timeframe", "required_timeframes"),
    )

    missing_symbols = sorted(required_symbols - available_symbols)
    if missing_symbols:
        raise ValueError(f"StrategyDossier requires unavailable symbols: {missing_symbols}")

    missing_timeframes = sorted(required_timeframes - available_timeframes)
    if missing_timeframes:
        raise ValueError(
            f"StrategyDossier requires unavailable timeframes: {missing_timeframes}"
        )


def _collect_optional_text_values(
    dossier: StrategyDossier,
    field_names: Sequence[str],
) -> set[str]:
    objects = (dossier, dossier.closure_record)
    values: set[str] = set()
    for item in objects:
        for field_name in field_names:
            if hasattr(item, field_name):
                values.update(_normalize_optional_texts(getattr(item, field_name)))
    return values


def _normalize_optional_texts(value: object) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, str):
        stripped = value.strip()
        return {stripped} if stripped else set()
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return {item.strip() for item in value if isinstance(item, str) and item.strip()}
    return set()


def _require_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _normalize_status_value(value: object) -> str:
    if hasattr(value, "value"):
        value = value.value
    if not isinstance(value, str):
        return ""
    return value.strip().lower()


def _deterministic_adapted_package_id(
    input_package_id: str,
    strategy_id: str,
    strategy_version: str,
) -> str:
    payload = {
        "input_package_id": input_package_id,
        "strategy_id": strategy_id,
        "strategy_version": strategy_version,
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return f"adapted-backtest-{digest[:16]}"
