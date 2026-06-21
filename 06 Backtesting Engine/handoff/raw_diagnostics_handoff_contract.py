"""Formal Motor B raw diagnostics handoff contract.

Block 12 closes and transfers the already-registered raw diagnostics artifact.
It does not create evidence, recalculate diagnostics, run simulation, score a
strategy, or change any readiness state.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

from registry.raw_diagnostics_registry import (
    REGISTRY_SCOPE,
    RawDiagnosticsRegistryRecord,
)


HANDOFF_SCOPE = "raw_diagnostics_handoff_only"
NON_APPROVAL_STATEMENT = (
    "This raw diagnostics handoff contract is not strategy validation, not "
    "performance evidence, not confidence evidence, not OOS evidence, not "
    "walk-forward evidence, not robustness evidence, not optimization evidence, "
    "not paper trading readiness, not production readiness, and not Stage 09 "
    "readiness."
)


@dataclass(frozen=True)
class RawDiagnosticsHandoffContract:
    handoff_contract_id: str
    registry_record_id: str
    diagnostics_id: str
    simulation_id: str
    package_id: str
    strategy_id: str
    strategy_version: str
    snapshot_id: str
    output_scope: str
    diagnostics_scope: str
    registry_scope: str
    simulation_status: str
    trade_count: int
    ending_capital: float
    return_pct: float
    handoff_scope: str
    non_approval_statement: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "handoff_contract_id": self.handoff_contract_id,
            "registry_record_id": self.registry_record_id,
            "diagnostics_id": self.diagnostics_id,
            "simulation_id": self.simulation_id,
            "package_id": self.package_id,
            "strategy_id": self.strategy_id,
            "strategy_version": self.strategy_version,
            "snapshot_id": self.snapshot_id,
            "output_scope": self.output_scope,
            "diagnostics_scope": self.diagnostics_scope,
            "registry_scope": self.registry_scope,
            "simulation_status": self.simulation_status,
            "trade_count": self.trade_count,
            "ending_capital": self.ending_capital,
            "return_pct": self.return_pct,
            "handoff_scope": self.handoff_scope,
            "non_approval_statement": self.non_approval_statement,
        }


def create_raw_diagnostics_handoff_contract(
    registry_record: RawDiagnosticsRegistryRecord,
) -> RawDiagnosticsHandoffContract:
    """Create the immutable Motor B raw diagnostics handoff contract."""

    _validate_registry_record(registry_record)
    return RawDiagnosticsHandoffContract(
        handoff_contract_id=_deterministic_handoff_contract_id(registry_record),
        registry_record_id=registry_record.registry_record_id,
        diagnostics_id=registry_record.diagnostics_id,
        simulation_id=registry_record.simulation_id,
        package_id=registry_record.package_id,
        strategy_id=registry_record.strategy_id,
        strategy_version=registry_record.strategy_version,
        snapshot_id=registry_record.snapshot_id,
        output_scope=registry_record.output_scope,
        diagnostics_scope=registry_record.diagnostics_scope,
        registry_scope=registry_record.registry_scope,
        simulation_status=registry_record.simulation_status,
        trade_count=registry_record.trade_count,
        ending_capital=registry_record.ending_capital,
        return_pct=registry_record.return_pct,
        handoff_scope=HANDOFF_SCOPE,
        non_approval_statement=NON_APPROVAL_STATEMENT,
    )


def _validate_registry_record(registry_record: RawDiagnosticsRegistryRecord) -> None:
    if registry_record.registry_scope != REGISTRY_SCOPE:
        raise ValueError("registry_scope must be raw_diagnostics_registry_only")
    if registry_record.simulation_status != "completed_raw_execution":
        raise ValueError("simulation_status must be completed_raw_execution")
    _require_equal(
        "simulation_id",
        registry_record.registry_created_from_simulation,
        registry_record.simulation_id,
    )
    _require_equal(
        "diagnostics_id",
        registry_record.registry_created_from_diagnostics,
        registry_record.diagnostics_id,
    )
    expected_registry_record_id = _deterministic_registry_record_id(registry_record)
    if registry_record.registry_record_id != expected_registry_record_id:
        raise ValueError("registry_record_id does not match registry lineage fields")


def _require_equal(field_name: str, left: str, right: str) -> None:
    if left != right:
        raise ValueError(f"{field_name} lineage must be internally consistent")


def _deterministic_handoff_contract_id(
    registry_record: RawDiagnosticsRegistryRecord,
) -> str:
    payload = {
        "registry_record_id": registry_record.registry_record_id,
        "diagnostics_id": registry_record.diagnostics_id,
        "simulation_id": registry_record.simulation_id,
        "package_id": registry_record.package_id,
        "strategy_id": registry_record.strategy_id,
        "strategy_version": registry_record.strategy_version,
        "snapshot_id": registry_record.snapshot_id,
        "output_scope": registry_record.output_scope,
        "diagnostics_scope": registry_record.diagnostics_scope,
        "registry_scope": registry_record.registry_scope,
        "simulation_status": registry_record.simulation_status,
    }
    return "raw-handoff-" + hashlib.sha256(
        _stable_json(payload).encode("utf-8")
    ).hexdigest()[:16]


def _deterministic_registry_record_id(
    registry_record: RawDiagnosticsRegistryRecord,
) -> str:
    payload = {
        "simulation_id": registry_record.simulation_id,
        "diagnostics_id": registry_record.diagnostics_id,
        "package_id": registry_record.package_id,
        "strategy_id": registry_record.strategy_id,
        "strategy_version": registry_record.strategy_version,
        "snapshot_id": registry_record.snapshot_id,
        "simulation_status": registry_record.simulation_status,
        "diagnostics_scope": registry_record.diagnostics_scope,
        "output_scope": registry_record.output_scope,
    }
    return "raw-registry-" + hashlib.sha256(
        _stable_json(payload).encode("utf-8")
    ).hexdigest()[:16]


def _stable_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
