"""Non-promotional diagnostics over raw execution scaffold output.

This layer consumes only SimulationResult objects with
output_scope="raw_execution_scaffold" and status COMPLETED_RAW_EXECUTION. The
diagnostics are descriptive mechanics only; they are not strategy validation,
not performance evidence, not confidence, not paper trading readiness, not OOS,
not walk-forward, and not robustness.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from simulation.gap_aware_simulation_core import SimulationResult, SimulationStatus


DIAGNOSTICS_SCOPE = "raw_scaffold_diagnostics_only"
NON_APPROVAL_STATEMENT = (
    "These raw scaffold diagnostics are not strategy validation, not performance "
    "evidence, not confidence, not OOS, not walk-forward, not robustness, and not "
    "paper trading readiness."
)


@dataclass(frozen=True)
class PerformanceDiagnosticsResult:
    simulation_id: str
    package_id: str
    strategy_id: str
    strategy_version: str
    snapshot_id: str
    diagnostics_scope: str
    non_approval_statement: str
    total_trade_count: int
    winning_trade_count: int
    losing_trade_count: int
    breakeven_trade_count: int
    gross_pnl: float
    net_pnl: float
    ending_capital: float
    return_pct: float
    total_fees_paid: float
    total_slippage_paid: float
    max_equity: float
    min_equity: float
    simple_max_drawdown_pct: float
    average_trade_net_pnl: float
    average_trade_duration_seconds: float
    gap_crossing_trade_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "simulation_id": self.simulation_id,
            "package_id": self.package_id,
            "strategy_id": self.strategy_id,
            "strategy_version": self.strategy_version,
            "snapshot_id": self.snapshot_id,
            "diagnostics_scope": self.diagnostics_scope,
            "non_approval_statement": self.non_approval_statement,
            "total_trade_count": self.total_trade_count,
            "winning_trade_count": self.winning_trade_count,
            "losing_trade_count": self.losing_trade_count,
            "breakeven_trade_count": self.breakeven_trade_count,
            "gross_pnl": self.gross_pnl,
            "net_pnl": self.net_pnl,
            "ending_capital": self.ending_capital,
            "return_pct": self.return_pct,
            "total_fees_paid": self.total_fees_paid,
            "total_slippage_paid": self.total_slippage_paid,
            "max_equity": self.max_equity,
            "min_equity": self.min_equity,
            "simple_max_drawdown_pct": self.simple_max_drawdown_pct,
            "average_trade_net_pnl": self.average_trade_net_pnl,
            "average_trade_duration_seconds": self.average_trade_duration_seconds,
            "gap_crossing_trade_count": self.gap_crossing_trade_count,
        }


def calculate_performance_diagnostics(
    simulation_result: SimulationResult,
) -> PerformanceDiagnosticsResult:
    """Calculate allowed descriptive diagnostics from raw scaffold output."""

    _validate_simulation_result(simulation_result)
    trades = simulation_result.trades
    total_trade_count = simulation_result.total_trade_count
    gross_pnl = sum(trade.gross_pnl for trade in trades)
    net_pnl = sum(trade.net_pnl for trade in trades)
    total_fees_paid = sum(trade.fees_paid for trade in trades)
    total_slippage_paid = sum(trade.slippage_paid for trade in trades)
    equity_values = [
        float(item["equity"])
        for item in simulation_result.equity_curve
        if "equity" in item and item["equity"] is not None
    ]
    if not equity_values:
        raise ValueError("equity_curve must contain at least one valid equity value")
    max_equity = max(equity_values)
    min_equity = min(equity_values)

    return PerformanceDiagnosticsResult(
        simulation_id=simulation_result.simulation_id,
        package_id=simulation_result.package_id,
        strategy_id=simulation_result.strategy_id,
        strategy_version=simulation_result.strategy_version,
        snapshot_id=simulation_result.snapshot_id,
        diagnostics_scope=DIAGNOSTICS_SCOPE,
        non_approval_statement=NON_APPROVAL_STATEMENT,
        total_trade_count=total_trade_count,
        winning_trade_count=simulation_result.total_winning_trades,
        losing_trade_count=simulation_result.total_losing_trades,
        breakeven_trade_count=simulation_result.total_breakeven_trades,
        gross_pnl=gross_pnl,
        net_pnl=net_pnl,
        ending_capital=simulation_result.ending_capital,
        return_pct=(
            (simulation_result.ending_capital - simulation_result.starting_capital)
            / simulation_result.starting_capital
        )
        * 100,
        total_fees_paid=total_fees_paid,
        total_slippage_paid=total_slippage_paid,
        max_equity=max_equity,
        min_equity=min_equity,
        simple_max_drawdown_pct=_simple_max_drawdown_pct(equity_values),
        average_trade_net_pnl=net_pnl / total_trade_count,
        average_trade_duration_seconds=_average_trade_duration_seconds(trades),
        gap_crossing_trade_count=sum(1 for trade in trades if trade.crosses_gap),
    )


def _validate_simulation_result(simulation_result: SimulationResult) -> None:
    if simulation_result.output_scope != "raw_execution_scaffold":
        raise ValueError("simulation_result output_scope must be raw_execution_scaffold")
    if simulation_result.simulation_status is SimulationStatus.COMPLETED:
        raise ValueError("legacy completed status is not accepted")
    if simulation_result.simulation_status is SimulationStatus.REJECTED:
        raise ValueError("rejected simulation results cannot produce diagnostics")
    if simulation_result.simulation_status in {
        SimulationStatus.INSUFFICIENT_INFORMATION,
        SimulationStatus.INSUFFICIENT_INFORMATION_NO_EXECUTABLE_SERIES,
    }:
        raise ValueError("insufficient information simulation results cannot produce diagnostics")
    if simulation_result.simulation_status is not SimulationStatus.COMPLETED_RAW_EXECUTION:
        raise ValueError("simulation_status must be completed_raw_execution")
    if not simulation_result.trades:
        raise ValueError("completed raw scaffold diagnostics require at least one trade")
    if simulation_result.total_trade_count != len(simulation_result.trades):
        raise ValueError("total_trade_count must match trades length")
    if (
        simulation_result.total_winning_trades
        + simulation_result.total_losing_trades
        + simulation_result.total_breakeven_trades
        != simulation_result.total_trade_count
    ):
        raise ValueError("trade outcome counts must sum to total_trade_count")
    if simulation_result.starting_capital <= 0:
        raise ValueError("starting_capital must be positive")
    if not simulation_result.equity_curve:
        raise ValueError("equity_curve must contain at least one point")


def _simple_max_drawdown_pct(equity_values: list[float]) -> float:
    peak = equity_values[0]
    max_drawdown = 0.0
    for value in equity_values:
        peak = max(peak, value)
        if peak > 0:
            drawdown = (peak - value) / peak
            max_drawdown = max(max_drawdown, drawdown)
    return max_drawdown * 100


def _average_trade_duration_seconds(trades) -> float:
    durations: list[float] = []
    for trade in trades:
        entry = _require_datetime(trade.entry_timestamp)
        exit_ = _require_datetime(trade.exit_timestamp)
        durations.append((exit_ - entry).total_seconds())
    return sum(durations) / len(durations)


def _require_datetime(value: object) -> datetime:
    if not isinstance(value, datetime):
        raise TypeError("trade timestamps must be datetime values")
    return value
