"""Deterministic registry for raw execution diagnostics.

Block 11 is archival and traceability-oriented. It records existing raw
execution scaffold output and existing raw scaffold diagnostics without
creating evidence, approvals, rankings, recommendations, or readiness changes.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

from metrics.performance_metrics_layer import (
    DIAGNOSTICS_SCOPE,
    PerformanceDiagnosticsResult,
)
from simulation.gap_aware_simulation_core import SimulationResult, SimulationStatus


REGISTRY_SCOPE = "raw_diagnostics_registry_only"
NON_APPROVAL_STATEMENT = (
    "This raw diagnostics registry record is not strategy validation, not "
    "performance evidence, not confidence evidence, not OOS evidence, not "
    "walk-forward evidence, not robustness evidence, not paper trading readiness, "
    "not production readiness, and not Stage 09 readiness."
)


@dataclass(frozen=True)
class RawDiagnosticsRegistryRecord:
    registry_record_id: str
    simulation_id: str
    diagnostics_id: str
    package_id: str
    strategy_id: str
    strategy_version: str
    snapshot_id: str
    simulation_status: str
    diagnostics_scope: str
    output_scope: str
    trade_count: int
    ending_capital: float
    return_pct: float
    registry_created_from_simulation: str
    registry_created_from_diagnostics: str
    registry_scope: str
    non_approval_statement: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "registry_record_id": self.registry_record_id,
            "simulation_id": self.simulation_id,
            "diagnostics_id": self.diagnostics_id,
            "package_id": self.package_id,
            "strategy_id": self.strategy_id,
            "strategy_version": self.strategy_version,
            "snapshot_id": self.snapshot_id,
            "simulation_status": self.simulation_status,
            "diagnostics_scope": self.diagnostics_scope,
            "output_scope": self.output_scope,
            "trade_count": self.trade_count,
            "ending_capital": self.ending_capital,
            "return_pct": self.return_pct,
            "registry_created_from_simulation": self.registry_created_from_simulation,
            "registry_created_from_diagnostics": self.registry_created_from_diagnostics,
            "registry_scope": self.registry_scope,
            "non_approval_statement": self.non_approval_statement,
        }


def create_raw_diagnostics_registry_record(
    simulation_result: SimulationResult,
    diagnostics_result: PerformanceDiagnosticsResult,
) -> RawDiagnosticsRegistryRecord:
    """Create an immutable registry record from existing raw outputs only."""

    _validate_inputs(simulation_result, diagnostics_result)
    diagnostics_id = _deterministic_diagnostics_id(diagnostics_result)
    registry_record_id = _deterministic_registry_record_id(
        simulation_result,
        diagnostics_result,
        diagnostics_id,
    )
    return RawDiagnosticsRegistryRecord(
        registry_record_id=registry_record_id,
        simulation_id=simulation_result.simulation_id,
        diagnostics_id=diagnostics_id,
        package_id=simulation_result.package_id,
        strategy_id=simulation_result.strategy_id,
        strategy_version=simulation_result.strategy_version,
        snapshot_id=simulation_result.snapshot_id,
        simulation_status=simulation_result.simulation_status.value,
        diagnostics_scope=diagnostics_result.diagnostics_scope,
        output_scope=simulation_result.output_scope,
        trade_count=simulation_result.total_trade_count,
        ending_capital=diagnostics_result.ending_capital,
        return_pct=diagnostics_result.return_pct,
        registry_created_from_simulation=simulation_result.simulation_id,
        registry_created_from_diagnostics=diagnostics_id,
        registry_scope=REGISTRY_SCOPE,
        non_approval_statement=NON_APPROVAL_STATEMENT,
    )


def _validate_inputs(
    simulation_result: SimulationResult,
    diagnostics_result: PerformanceDiagnosticsResult,
) -> None:
    if simulation_result.output_scope != "raw_execution_scaffold":
        raise ValueError("simulation output_scope must be raw_execution_scaffold")
    if diagnostics_result.diagnostics_scope != DIAGNOSTICS_SCOPE:
        raise ValueError("diagnostics_scope must be raw_scaffold_diagnostics_only")
    if simulation_result.simulation_status is SimulationStatus.COMPLETED:
        raise ValueError("legacy completed simulation status is not accepted")
    if simulation_result.simulation_status is SimulationStatus.REJECTED:
        raise ValueError("rejected simulation results cannot be registered")
    if simulation_result.simulation_status in {
        SimulationStatus.INSUFFICIENT_INFORMATION,
        SimulationStatus.INSUFFICIENT_INFORMATION_NO_EXECUTABLE_SERIES,
    }:
        raise ValueError("insufficient information simulation results cannot be registered")
    if simulation_result.simulation_status is not SimulationStatus.COMPLETED_RAW_EXECUTION:
        raise ValueError("simulation_status must be completed_raw_execution")
    _require_matching_identity(
        "simulation_id",
        simulation_result.simulation_id,
        diagnostics_result.simulation_id,
    )
    _require_matching_identity(
        "package_id",
        simulation_result.package_id,
        diagnostics_result.package_id,
    )
    _require_matching_identity(
        "strategy_id",
        simulation_result.strategy_id,
        diagnostics_result.strategy_id,
    )
    _require_matching_identity(
        "strategy_version",
        simulation_result.strategy_version,
        diagnostics_result.strategy_version,
    )
    _require_matching_identity(
        "snapshot_id",
        simulation_result.snapshot_id,
        diagnostics_result.snapshot_id,
    )


def _require_matching_identity(field_name: str, left: str, right: str) -> None:
    if left != right:
        raise ValueError(f"{field_name} must match between simulation and diagnostics")


def _deterministic_diagnostics_id(
    diagnostics_result: PerformanceDiagnosticsResult,
) -> str:
    payload = _stable_json(diagnostics_result.to_dict())
    return "raw-diagnostics-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _deterministic_registry_record_id(
    simulation_result: SimulationResult,
    diagnostics_result: PerformanceDiagnosticsResult,
    diagnostics_id: str,
) -> str:
    payload = {
        "simulation_id": simulation_result.simulation_id,
        "diagnostics_id": diagnostics_id,
        "package_id": simulation_result.package_id,
        "strategy_id": simulation_result.strategy_id,
        "strategy_version": simulation_result.strategy_version,
        "snapshot_id": simulation_result.snapshot_id,
        "simulation_status": simulation_result.simulation_status.value,
        "diagnostics_scope": diagnostics_result.diagnostics_scope,
        "output_scope": simulation_result.output_scope,
    }
    return "raw-registry-" + hashlib.sha256(
        _stable_json(payload).encode("utf-8")
    ).hexdigest()[:16]


def _stable_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
