from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

import pytest


BACKTESTING_ROOT = Path(__file__).resolve().parents[1]
if str(BACKTESTING_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKTESTING_ROOT))

from metrics.performance_metrics_layer import (  # noqa: E402
    DIAGNOSTICS_SCOPE,
    PerformanceDiagnosticsResult,
)
from registry.raw_diagnostics_registry import (  # noqa: E402
    NON_APPROVAL_STATEMENT,
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


def _simulation_result(
    *,
    simulation_status: SimulationStatus = SimulationStatus.COMPLETED_RAW_EXECUTION,
    output_scope: str = "raw_execution_scaffold",
    package_id: str = "pkg-1",
    strategy_id: str = "strategy-1",
    strategy_version: str = "1.0.0",
    snapshot_id: str = "snapshot-1",
) -> SimulationResult:
    return SimulationResult(
        simulation_id="sim-1",
        package_id=package_id,
        strategy_id=strategy_id,
        strategy_version=strategy_version,
        snapshot_id=snapshot_id,
        simulation_status=simulation_status,
        output_scope=output_scope,
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


def _diagnostics_result(
    *,
    simulation_id: str = "sim-1",
    diagnostics_scope: str = DIAGNOSTICS_SCOPE,
    package_id: str = "pkg-1",
    strategy_id: str = "strategy-1",
    strategy_version: str = "1.0.0",
    snapshot_id: str = "snapshot-1",
) -> PerformanceDiagnosticsResult:
    return PerformanceDiagnosticsResult(
        simulation_id=simulation_id,
        package_id=package_id,
        strategy_id=strategy_id,
        strategy_version=strategy_version,
        snapshot_id=snapshot_id,
        diagnostics_scope=diagnostics_scope,
        non_approval_statement="diagnostics are non-approval raw scaffold diagnostics",
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


def test_valid_registry_creation() -> None:
    record = _registry_record()

    assert record.registry_scope == REGISTRY_SCOPE
    assert record.simulation_id == "sim-1"
    assert record.package_id == "pkg-1"
    assert record.strategy_id == "strategy-1"
    assert record.strategy_version == "1.0.0"
    assert record.snapshot_id == "snapshot-1"
    assert record.simulation_status == "completed_raw_execution"
    assert record.output_scope == "raw_execution_scaffold"
    assert record.diagnostics_scope == DIAGNOSTICS_SCOPE
    assert record.trade_count == 1
    assert record.ending_capital == 108.0
    assert record.return_pct == 8.0


def test_reject_wrong_simulation_scope() -> None:
    with pytest.raises(ValueError, match="output_scope"):
        create_raw_diagnostics_registry_record(
            _simulation_result(output_scope="strategy_backtest"),
            _diagnostics_result(),
        )


def test_reject_wrong_diagnostics_scope() -> None:
    with pytest.raises(ValueError, match="diagnostics_scope"):
        create_raw_diagnostics_registry_record(
            _simulation_result(),
            _diagnostics_result(diagnostics_scope="performance_evidence"),
        )


def test_reject_rejected_simulation() -> None:
    with pytest.raises(ValueError, match="rejected"):
        create_raw_diagnostics_registry_record(
            _simulation_result(simulation_status=SimulationStatus.REJECTED),
            _diagnostics_result(),
        )


def test_reject_insufficient_information_simulation() -> None:
    with pytest.raises(ValueError, match="insufficient information"):
        create_raw_diagnostics_registry_record(
            _simulation_result(simulation_status=SimulationStatus.INSUFFICIENT_INFORMATION),
            _diagnostics_result(),
        )


def test_reject_no_executable_series_simulation() -> None:
    with pytest.raises(ValueError, match="insufficient information"):
        create_raw_diagnostics_registry_record(
            _simulation_result(
                simulation_status=(
                    SimulationStatus.INSUFFICIENT_INFORMATION_NO_EXECUTABLE_SERIES
                )
            ),
            _diagnostics_result(),
        )


def test_reject_legacy_completed_simulation() -> None:
    with pytest.raises(ValueError, match="legacy completed"):
        create_raw_diagnostics_registry_record(
            _simulation_result(simulation_status=SimulationStatus.COMPLETED),
            _diagnostics_result(),
        )


def test_reject_simulation_id_mismatch() -> None:
    with pytest.raises(ValueError, match="simulation_id"):
        create_raw_diagnostics_registry_record(
            _simulation_result(),
            _diagnostics_result(simulation_id="other-simulation"),
        )


def test_reject_package_mismatch() -> None:
    with pytest.raises(ValueError, match="package_id"):
        create_raw_diagnostics_registry_record(
            _simulation_result(),
            _diagnostics_result(package_id="other-package"),
        )


def test_reject_strategy_mismatch() -> None:
    with pytest.raises(ValueError, match="strategy_id"):
        create_raw_diagnostics_registry_record(
            _simulation_result(),
            _diagnostics_result(strategy_id="other-strategy"),
        )


def test_reject_strategy_version_mismatch() -> None:
    with pytest.raises(ValueError, match="strategy_version"):
        create_raw_diagnostics_registry_record(
            _simulation_result(),
            _diagnostics_result(strategy_version="2.0.0"),
        )


def test_reject_snapshot_mismatch() -> None:
    with pytest.raises(ValueError, match="snapshot_id"):
        create_raw_diagnostics_registry_record(
            _simulation_result(),
            _diagnostics_result(snapshot_id="other-snapshot"),
        )


def test_deterministic_registry_id() -> None:
    first = _registry_record()
    second = _registry_record()

    assert first.registry_record_id == second.registry_record_id
    assert first.diagnostics_id == second.diagnostics_id


def test_frozen_dataclass_enforcement() -> None:
    record = _registry_record()

    with pytest.raises(FrozenInstanceError):
        record.registry_scope = "changed"


def test_no_mutation_of_inputs() -> None:
    simulation = _simulation_result()
    diagnostics = _diagnostics_result()
    simulation_before = simulation.to_dict()
    diagnostics_before = diagnostics.to_dict()

    create_raw_diagnostics_registry_record(simulation, diagnostics)

    assert simulation.to_dict() == simulation_before
    assert diagnostics.to_dict() == diagnostics_before


def test_serialization_works() -> None:
    record = _registry_record()
    serialized = record.to_dict()

    assert serialized["registry_record_id"] == record.registry_record_id
    assert serialized["registry_scope"] == REGISTRY_SCOPE
    assert serialized["registry_created_from_simulation"] == "sim-1"
    assert serialized["registry_created_from_diagnostics"] == record.diagnostics_id


def test_non_approval_statement_exists() -> None:
    record = _registry_record()

    assert record.non_approval_statement == NON_APPROVAL_STATEMENT
    assert "not strategy validation" in record.non_approval_statement
    assert "not performance evidence" in record.non_approval_statement
    assert "not confidence evidence" in record.non_approval_statement
    assert "not OOS evidence" in record.non_approval_statement
    assert "not walk-forward evidence" in record.non_approval_statement
    assert "not robustness evidence" in record.non_approval_statement
    assert "not paper trading readiness" in record.non_approval_statement
    assert "not production readiness" in record.non_approval_statement
    assert "not Stage 09 readiness" in record.non_approval_statement


def test_registry_scope_correct() -> None:
    assert _registry_record().registry_scope == "raw_diagnostics_registry_only"


def test_no_readiness_fields_introduced() -> None:
    keys = set(_registry_record().to_dict())

    assert "stage_09_readiness" not in keys
    assert "paper_trading_readiness" not in keys
    assert "production_readiness" not in keys


def test_no_evidence_package_fields_introduced() -> None:
    keys = set(_registry_record().to_dict())

    assert "evidence_package" not in keys
    assert "evidence_package_id" not in keys


def test_no_forbidden_scoring_fields() -> None:
    record = _registry_record()
    field_names = {field.name.lower() for field in fields(record)}
    keys = {key.lower() for key in record.to_dict()}
    forbidden = {
        "score",
        "ranking",
        "confidence_score",
        "approval_status",
        "promotion_status",
        "recommendation",
    }

    assert forbidden.isdisjoint(field_names)
    assert forbidden.isdisjoint(keys)


def test_registry_reproduces_identical_output_across_repeated_runs() -> None:
    first = _registry_record()
    second = _registry_record()

    assert first == second
    assert first.to_dict() == second.to_dict()


def test_registry_created_from_fields_reference_source_outputs() -> None:
    simulation = _simulation_result()
    diagnostics = _diagnostics_result()
    record = create_raw_diagnostics_registry_record(simulation, diagnostics)

    assert record.registry_created_from_simulation == simulation.simulation_id
    assert record.registry_created_from_diagnostics == record.diagnostics_id
    assert record.trade_count == diagnostics.total_trade_count
    assert record.ending_capital == diagnostics.ending_capital
    assert record.return_pct == diagnostics.return_pct


def test_no_metric_recalculation_side_effect_from_altered_diagnostics() -> None:
    simulation = _simulation_result()
    diagnostics = replace(_diagnostics_result(), return_pct=99.0, ending_capital=199.0)

    record = create_raw_diagnostics_registry_record(simulation, diagnostics)

    assert record.return_pct == 99.0
    assert record.ending_capital == 199.0
