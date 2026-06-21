from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

import pytest


BACKTESTING_ROOT = Path(__file__).resolve().parents[1]
if str(BACKTESTING_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKTESTING_ROOT))

from handoff.raw_diagnostics_handoff_contract import (  # noqa: E402
    HANDOFF_SCOPE,
    NON_APPROVAL_STATEMENT,
    RawDiagnosticsHandoffContract,
    create_raw_diagnostics_handoff_contract,
)
from metrics.performance_metrics_layer import (  # noqa: E402
    DIAGNOSTICS_SCOPE,
    PerformanceDiagnosticsResult,
)
from registry.raw_diagnostics_registry import (  # noqa: E402
    REGISTRY_SCOPE,
    RawDiagnosticsRegistryRecord,
    create_raw_diagnostics_registry_record,
)
from simulation.gap_aware_simulation_core import (  # noqa: E402
    PositionState,
    SimulationResult,
    SimulationStatus,
    TradeRecord,
)


BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _trade() -> TradeRecord:
    return TradeRecord(
        trade_id="trade-1",
        symbol="BTCUSDT",
        timeframe="1d",
        entry_timestamp=BASE_TIME,
        exit_timestamp=BASE_TIME + timedelta(days=1),
        entry_price=100.0,
        exit_price=110.0,
        quantity=1.0,
        direction=PositionState.LONG,
        fees_paid=1.0,
        slippage_paid=1.0,
        gross_pnl=10.0,
        net_pnl=8.0,
        expected_time_delta="1 day, 0:00:00",
        detected_gap_count=0,
        max_gap_multiple=1.0,
        crosses_gap=False,
    )


def _simulation_result() -> SimulationResult:
    return SimulationResult(
        simulation_id="sim-1",
        package_id="pkg-1",
        strategy_id="strategy-1",
        strategy_version="1.0.0",
        snapshot_id="snapshot-1",
        simulation_status=SimulationStatus.COMPLETED_RAW_EXECUTION,
        output_scope="raw_execution_scaffold",
        simulation_reason="Raw execution scaffold completed.",
        starting_capital=100.0,
        ending_capital=108.0,
        equity_curve=(
            {"timestamp": BASE_TIME.isoformat(), "equity": 100.0},
            {"timestamp": (BASE_TIME + timedelta(days=1)).isoformat(), "equity": 108.0},
        ),
        trades=(_trade(),),
        total_trade_count=1,
        total_winning_trades=1,
        total_losing_trades=0,
        total_breakeven_trades=0,
        assumptions_reference="assumptions-1",
        governance_reference="governance-1",
        temporal_reference="temporal-1",
    )


def _diagnostics_result() -> PerformanceDiagnosticsResult:
    return PerformanceDiagnosticsResult(
        simulation_id="sim-1",
        package_id="pkg-1",
        strategy_id="strategy-1",
        strategy_version="1.0.0",
        snapshot_id="snapshot-1",
        diagnostics_scope=DIAGNOSTICS_SCOPE,
        non_approval_statement="raw scaffold diagnostics only",
        total_trade_count=1,
        winning_trade_count=1,
        losing_trade_count=0,
        breakeven_trade_count=0,
        gross_pnl=10.0,
        net_pnl=8.0,
        ending_capital=108.0,
        return_pct=8.0,
        total_fees_paid=1.0,
        total_slippage_paid=1.0,
        max_equity=108.0,
        min_equity=100.0,
        simple_max_drawdown_pct=0.0,
        average_trade_net_pnl=8.0,
        average_trade_duration_seconds=86400.0,
        gap_crossing_trade_count=0,
    )


def _registry_record() -> RawDiagnosticsRegistryRecord:
    return create_raw_diagnostics_registry_record(
        _simulation_result(),
        _diagnostics_result(),
    )


def _handoff_contract() -> RawDiagnosticsHandoffContract:
    return create_raw_diagnostics_handoff_contract(_registry_record())


def test_golden_path() -> None:
    contract = _handoff_contract()
    registry_record = _registry_record()

    assert contract.handoff_scope == HANDOFF_SCOPE
    assert contract.registry_record_id == registry_record.registry_record_id
    assert contract.diagnostics_id == registry_record.diagnostics_id
    assert contract.simulation_id == "sim-1"
    assert contract.package_id == "pkg-1"
    assert contract.strategy_id == "strategy-1"
    assert contract.strategy_version == "1.0.0"
    assert contract.snapshot_id == "snapshot-1"
    assert contract.output_scope == "raw_execution_scaffold"
    assert contract.diagnostics_scope == DIAGNOSTICS_SCOPE
    assert contract.registry_scope == REGISTRY_SCOPE
    assert contract.simulation_status == "completed_raw_execution"
    assert contract.trade_count == 1
    assert contract.ending_capital == 108.0
    assert contract.return_pct == 8.0


def test_reject_wrong_registry_scope() -> None:
    registry_record = replace(_registry_record(), registry_scope="evidence_registry")

    with pytest.raises(ValueError, match="registry_scope"):
        create_raw_diagnostics_handoff_contract(registry_record)


@pytest.mark.parametrize(
    "simulation_status",
    (
        "rejected",
        "insufficient_information",
        "insufficient_information_no_executable_series",
        "completed",
    ),
)
def test_reject_invalid_simulation_statuses(simulation_status: str) -> None:
    registry_record = replace(_registry_record(), simulation_status=simulation_status)

    with pytest.raises(ValueError, match="simulation_status"):
        create_raw_diagnostics_handoff_contract(registry_record)


@pytest.mark.parametrize(
    "field_name",
    (
        "package_id",
        "strategy_id",
        "strategy_version",
        "snapshot_id",
    ),
)
def test_reject_registry_record_id_lineage_mismatch(field_name: str) -> None:
    registry_record = replace(_registry_record(), **{field_name: "mismatch"})

    with pytest.raises(ValueError, match="registry_record_id"):
        create_raw_diagnostics_handoff_contract(registry_record)


def test_reject_simulation_id_mismatch() -> None:
    registry_record = replace(_registry_record(), simulation_id="mismatch")

    with pytest.raises(ValueError, match="simulation_id|registry_record_id"):
        create_raw_diagnostics_handoff_contract(registry_record)


def test_reject_diagnostics_id_mismatch() -> None:
    registry_record = replace(_registry_record(), diagnostics_id="mismatch")

    with pytest.raises(ValueError, match="diagnostics_id|registry_record_id"):
        create_raw_diagnostics_handoff_contract(registry_record)


def test_reject_registry_created_from_simulation_mismatch() -> None:
    registry_record = replace(
        _registry_record(),
        registry_created_from_simulation="mismatch",
    )

    with pytest.raises(ValueError, match="simulation_id"):
        create_raw_diagnostics_handoff_contract(registry_record)


def test_reject_registry_created_from_diagnostics_mismatch() -> None:
    registry_record = replace(
        _registry_record(),
        registry_created_from_diagnostics="mismatch",
    )

    with pytest.raises(ValueError, match="diagnostics_id"):
        create_raw_diagnostics_handoff_contract(registry_record)


def test_deterministic_handoff_contract_id() -> None:
    first = _handoff_contract()
    second = _handoff_contract()

    assert first.handoff_contract_id == second.handoff_contract_id
    assert first == second


def test_frozen_dataclass_enforcement() -> None:
    contract = _handoff_contract()

    with pytest.raises(FrozenInstanceError):
        contract.handoff_scope = "changed"


def test_serialization_correctness() -> None:
    contract = _handoff_contract()
    serialized = contract.to_dict()

    assert serialized["handoff_contract_id"] == contract.handoff_contract_id
    assert serialized["handoff_scope"] == HANDOFF_SCOPE
    assert serialized["registry_record_id"] == contract.registry_record_id
    assert serialized["simulation_status"] == "completed_raw_execution"
    assert serialized["trade_count"] == 1


def test_no_mutation_of_inputs() -> None:
    registry_record = _registry_record()
    before = registry_record.to_dict()

    create_raw_diagnostics_handoff_contract(registry_record)

    assert registry_record.to_dict() == before


def test_non_approval_statement_verification() -> None:
    contract = _handoff_contract()

    assert contract.non_approval_statement == NON_APPROVAL_STATEMENT
    assert "not strategy validation" in contract.non_approval_statement
    assert "not performance evidence" in contract.non_approval_statement
    assert "not confidence evidence" in contract.non_approval_statement
    assert "not OOS evidence" in contract.non_approval_statement
    assert "not walk-forward evidence" in contract.non_approval_statement
    assert "not robustness evidence" in contract.non_approval_statement
    assert "not optimization evidence" in contract.non_approval_statement
    assert "not paper trading readiness" in contract.non_approval_statement
    assert "not production readiness" in contract.non_approval_statement
    assert "not Stage 09 readiness" in contract.non_approval_statement


def test_no_forbidden_fields_introduced() -> None:
    contract = _handoff_contract()
    field_names = {field.name.lower() for field in fields(contract)}
    keys = {key.lower() for key in contract.to_dict()}
    forbidden = {
        "readiness",
        "confidence",
        "evidence_package",
        "ranking",
        "score",
        "promotion",
        "sharpe",
        "sortino",
        "calmar",
        "cagr",
        "alpha",
        "beta",
    }

    assert forbidden.isdisjoint(field_names)
    assert forbidden.isdisjoint(keys)


def test_reproduces_identical_output_across_repeated_runs() -> None:
    first = create_raw_diagnostics_handoff_contract(_registry_record())
    second = create_raw_diagnostics_handoff_contract(_registry_record())

    assert first.to_dict() == second.to_dict()
