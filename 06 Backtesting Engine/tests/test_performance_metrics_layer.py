from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

import pandas as pd
import pytest


BACKTESTING_ROOT = Path(__file__).resolve().parents[1]
if str(BACKTESTING_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKTESTING_ROOT))

from metrics.performance_metrics_layer import (  # noqa: E402
    DIAGNOSTICS_SCOPE,
    NON_APPROVAL_STATEMENT,
    PerformanceDiagnosticsResult,
    calculate_performance_diagnostics,
)
from simulation.gap_aware_simulation_core import (  # noqa: E402
    PositionState,
    SimulationResult,
    SimulationStatus,
    TradeRecord,
)


BASE_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _trade(
    *,
    trade_id: str = "trade-1",
    entry_offset_days: int = 0,
    exit_offset_days: int = 1,
    gross_pnl: float = 10.0,
    net_pnl: float = 8.0,
    fees_paid: float = 1.0,
    slippage_paid: float = 1.0,
    crosses_gap: bool = False,
) -> TradeRecord:
    return TradeRecord(
        trade_id=trade_id,
        symbol="BTCUSDT",
        timeframe="1d",
        entry_timestamp=BASE_TIME + timedelta(days=entry_offset_days),
        exit_timestamp=BASE_TIME + timedelta(days=exit_offset_days),
        entry_price=100.0,
        exit_price=110.0,
        quantity=1.0,
        direction=PositionState.LONG,
        fees_paid=fees_paid,
        slippage_paid=slippage_paid,
        gross_pnl=gross_pnl,
        net_pnl=net_pnl,
        expected_time_delta="1 day, 0:00:00",
        detected_gap_count=1 if crosses_gap else 0,
        max_gap_multiple=2.0 if crosses_gap else 1.0,
        crosses_gap=crosses_gap,
    )


def _simulation_result(
    *,
    simulation_status: SimulationStatus = SimulationStatus.COMPLETED_RAW_EXECUTION,
    output_scope: str = "raw_execution_scaffold",
    trades: tuple[TradeRecord, ...] | None = None,
    starting_capital: float = 100.0,
    ending_capital: float = 108.0,
    equity_curve: tuple[dict[str, object], ...] | None = None,
) -> SimulationResult:
    if trades is None:
        trades = (_trade(),)
    if equity_curve is None:
        equity_curve = (
            {"timestamp": BASE_TIME.isoformat(), "equity": starting_capital},
            {
                "timestamp": (BASE_TIME + timedelta(days=1)).isoformat(),
                "equity": ending_capital,
            },
        )
    winning = sum(1 for trade in trades if trade.net_pnl > 0)
    losing = sum(1 for trade in trades if trade.net_pnl < 0)
    breakeven = sum(1 for trade in trades if trade.net_pnl == 0)
    return SimulationResult(
        simulation_id="sim-1",
        package_id="pkg-1",
        strategy_id="strategy-1",
        strategy_version="1.0.0",
        snapshot_id="snapshot-1",
        simulation_status=simulation_status,
        output_scope=output_scope,
        simulation_reason="Raw execution scaffold completed.",
        starting_capital=starting_capital,
        ending_capital=ending_capital,
        equity_curve=equity_curve,
        trades=trades,
        total_trade_count=len(trades),
        total_winning_trades=winning,
        total_losing_trades=losing,
        total_breakeven_trades=breakeven,
        assumptions_reference="assumptions-1",
        governance_reference="governance-1",
        temporal_reference="temporal-1",
    )


def test_valid_raw_execution_scaffold_produces_diagnostics() -> None:
    result = calculate_performance_diagnostics(_simulation_result())

    assert result.diagnostics_scope == DIAGNOSTICS_SCOPE
    assert result.simulation_id == "sim-1"
    assert result.package_id == "pkg-1"
    assert result.strategy_id == "strategy-1"
    assert result.strategy_version == "1.0.0"
    assert result.snapshot_id == "snapshot-1"


def test_reject_wrong_output_scope() -> None:
    simulation_result = _simulation_result(output_scope="strategy_backtest")

    with pytest.raises(ValueError, match="output_scope"):
        calculate_performance_diagnostics(simulation_result)


def test_reject_rejected_simulation() -> None:
    simulation_result = _simulation_result(simulation_status=SimulationStatus.REJECTED)

    with pytest.raises(ValueError, match="rejected"):
        calculate_performance_diagnostics(simulation_result)


def test_reject_insufficient_information_simulation() -> None:
    simulation_result = _simulation_result(
        simulation_status=SimulationStatus.INSUFFICIENT_INFORMATION
    )

    with pytest.raises(ValueError, match="insufficient information"):
        calculate_performance_diagnostics(simulation_result)


def test_reject_legacy_completed_status_if_present() -> None:
    simulation_result = _simulation_result(simulation_status=SimulationStatus.COMPLETED)

    with pytest.raises(ValueError, match="legacy completed"):
        calculate_performance_diagnostics(simulation_result)


def test_counts_match_simulation_result_trade_counts() -> None:
    trades = (
        _trade(trade_id="trade-1", net_pnl=8.0),
        _trade(trade_id="trade-2", net_pnl=-3.0),
        _trade(trade_id="trade-3", net_pnl=0.0),
    )

    result = calculate_performance_diagnostics(_simulation_result(trades=trades))

    assert result.total_trade_count == 3
    assert result.winning_trade_count == 1
    assert result.losing_trade_count == 1
    assert result.breakeven_trade_count == 1


def test_gross_and_net_pnl_calculated_from_trades() -> None:
    trades = (
        _trade(trade_id="trade-1", gross_pnl=10.0, net_pnl=8.0),
        _trade(trade_id="trade-2", gross_pnl=-5.0, net_pnl=-7.0),
    )

    result = calculate_performance_diagnostics(_simulation_result(trades=trades))

    assert result.gross_pnl == 5.0
    assert result.net_pnl == 1.0
    assert result.average_trade_net_pnl == 0.5


def test_fees_and_slippage_totals_calculated_correctly() -> None:
    trades = (
        _trade(trade_id="trade-1", fees_paid=1.25, slippage_paid=2.5),
        _trade(trade_id="trade-2", fees_paid=0.75, slippage_paid=1.5),
    )

    result = calculate_performance_diagnostics(_simulation_result(trades=trades))

    assert result.total_fees_paid == 2.0
    assert result.total_slippage_paid == 4.0


def test_return_pct_calculated_from_starting_and_ending_capital() -> None:
    result = calculate_performance_diagnostics(
        _simulation_result(starting_capital=100.0, ending_capital=112.5)
    )

    assert result.ending_capital == 112.5
    assert result.return_pct == 12.5


def test_breakeven_trades_handled_correctly() -> None:
    trades = (
        _trade(trade_id="trade-1", gross_pnl=0.0, net_pnl=0.0),
        _trade(trade_id="trade-2", gross_pnl=5.0, net_pnl=4.0),
    )

    result = calculate_performance_diagnostics(_simulation_result(trades=trades))

    assert result.breakeven_trade_count == 1
    assert result.winning_trade_count == 1
    assert result.losing_trade_count == 0


def test_gap_crossing_count_calculated_from_trade_records() -> None:
    trades = (
        _trade(trade_id="trade-1", crosses_gap=True),
        _trade(trade_id="trade-2", crosses_gap=False),
        _trade(trade_id="trade-3", crosses_gap=True),
    )

    result = calculate_performance_diagnostics(_simulation_result(trades=trades))

    assert result.gap_crossing_trade_count == 2


def test_simple_max_drawdown_calculated_from_equity_curve() -> None:
    equity_curve = (
        {"timestamp": BASE_TIME.isoformat(), "equity": 100.0},
        {"timestamp": (BASE_TIME + timedelta(days=1)).isoformat(), "equity": 110.0},
        {"timestamp": (BASE_TIME + timedelta(days=2)).isoformat(), "equity": 99.0},
        {"timestamp": (BASE_TIME + timedelta(days=3)).isoformat(), "equity": 105.0},
    )

    result = calculate_performance_diagnostics(
        _simulation_result(equity_curve=equity_curve, ending_capital=105.0)
    )

    assert result.max_equity == 110.0
    assert result.min_equity == 99.0
    assert result.simple_max_drawdown_pct == 10.0


def test_empty_trades_rejected_unless_status_is_insufficient() -> None:
    completed_empty = _simulation_result(trades=())
    insufficient_empty = _simulation_result(
        simulation_status=SimulationStatus.INSUFFICIENT_INFORMATION,
        trades=(),
    )

    with pytest.raises(ValueError, match="at least one trade"):
        calculate_performance_diagnostics(completed_empty)
    with pytest.raises(ValueError, match="insufficient information"):
        calculate_performance_diagnostics(insufficient_empty)


def test_deterministic_output() -> None:
    simulation_result = _simulation_result()

    first = calculate_performance_diagnostics(simulation_result)
    second = calculate_performance_diagnostics(simulation_result)

    assert first == second
    assert first.to_dict() == second.to_dict()


def test_frozen_dataclass_enforcement() -> None:
    result = calculate_performance_diagnostics(_simulation_result())

    with pytest.raises(FrozenInstanceError):
        result.net_pnl = 1.0


def test_no_mutation_of_simulation_result() -> None:
    simulation_result = _simulation_result()
    before = simulation_result.to_dict()

    calculate_performance_diagnostics(simulation_result)

    assert simulation_result.to_dict() == before


def test_no_parquet_loading(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_read_parquet(*args: object, **kwargs: object) -> None:
        raise AssertionError("read_parquet must not be called by diagnostics layer")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    result = calculate_performance_diagnostics(_simulation_result())

    assert result.total_trade_count == 1


def test_no_forbidden_metrics_fields() -> None:
    result = calculate_performance_diagnostics(_simulation_result())
    names = {field.name.lower() for field in fields(result)}
    serialized_keys = {key.lower() for key in result.to_dict()}
    forbidden = {
        "sharpe",
        "sortino",
        "calmar",
        "cagr",
        "alpha",
        "beta",
        "information_ratio",
        "confidence",
        "oos",
        "walk_forward",
        "robustness",
        "ranking_score",
        "strategy_score",
    }

    assert forbidden.isdisjoint(names)
    assert forbidden.isdisjoint(serialized_keys)


def test_diagnostics_result_includes_non_approval_statement() -> None:
    result = calculate_performance_diagnostics(_simulation_result())

    assert result.non_approval_statement == NON_APPROVAL_STATEMENT
    assert "not strategy validation" in result.non_approval_statement
    assert "not performance evidence" in result.non_approval_statement
    assert "not confidence" in result.non_approval_statement
    assert "not OOS" in result.non_approval_statement
    assert "not walk-forward" in result.non_approval_statement
    assert "not robustness" in result.non_approval_statement
    assert "not paper trading readiness" in result.non_approval_statement


def test_diagnostics_result_does_not_change_readiness() -> None:
    simulation_result = _simulation_result()

    result = calculate_performance_diagnostics(simulation_result)

    assert simulation_result.to_dict() == _simulation_result().to_dict()
    assert "readiness" not in result.to_dict()
    assert "stage_09" not in result.to_dict()
    assert "paper_trading" not in result.to_dict()


def test_average_trade_duration_seconds_calculated() -> None:
    trades = (
        _trade(trade_id="trade-1", entry_offset_days=0, exit_offset_days=1),
        _trade(trade_id="trade-2", entry_offset_days=1, exit_offset_days=3),
    )

    result = calculate_performance_diagnostics(_simulation_result(trades=trades))

    assert result.average_trade_duration_seconds == 129600.0


def test_reject_inconsistent_trade_outcome_counts() -> None:
    simulation_result = replace(_simulation_result(), total_winning_trades=0)

    with pytest.raises(ValueError, match="trade outcome counts"):
        calculate_performance_diagnostics(simulation_result)
