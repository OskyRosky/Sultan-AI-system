"""Raw execution scaffold for 06B Block 09.

This is an infrastructure execution scaffold, not a full strategic backtesting
engine and not StrategyDossier strategy validation. It loads only
package-declared Parquet paths and produces raw trade lifecycle and equity
state. It does not create performance evidence, confidence evidence, analytic
summary modules, rankings, readiness changes, or evidence packages.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import hashlib
import json
from pathlib import Path
from typing import Any

import pandas as pd

from adapters.strategy_dossier_adapter import AdaptedBacktestPackage
from assumptions.execution_assumptions import (
    ExecutionAssumptionSet,
    FeeModelType,
    OrderExecutionTiming,
    SlippageModelType,
    validate_execution_assumption_set,
)
from governance.pre_execution_governance_gate import (
    GovernanceGateResult,
    GovernanceGateStatus,
)
from validators.temporal_admissibility_validator import (
    TemporalAdmissibilityResult,
    TemporalAdmissibilityStatus,
)


class SimulationStatus(str, Enum):
    """Raw scaffold status values.

    COMPLETED is legacy/deprecated and must not be emitted by Block 09.
    Successful raw scaffold output must use COMPLETED_RAW_EXECUTION.
    """

    COMPLETED = "completed"
    COMPLETED_RAW_EXECUTION = "completed_raw_execution"
    REJECTED = "rejected"
    INSUFFICIENT_INFORMATION = "insufficient_information"
    INSUFFICIENT_INFORMATION_NO_EXECUTABLE_SERIES = (
        "insufficient_information_no_executable_series"
    )


class PositionState(str, Enum):
    FLAT = "flat"
    LONG = "long"
    SHORT = "short"


@dataclass(frozen=True)
class TradeRecord:
    trade_id: str
    symbol: str
    timeframe: str
    entry_timestamp: datetime
    exit_timestamp: datetime
    entry_price: float
    exit_price: float
    quantity: float
    direction: PositionState
    fees_paid: float
    slippage_paid: float
    gross_pnl: float
    net_pnl: float
    expected_time_delta: str | None
    detected_gap_count: int
    max_gap_multiple: float
    crosses_gap: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "trade_id": self.trade_id,
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "entry_timestamp": self.entry_timestamp.isoformat(),
            "exit_timestamp": self.exit_timestamp.isoformat(),
            "entry_price": self.entry_price,
            "exit_price": self.exit_price,
            "quantity": self.quantity,
            "direction": self.direction.value,
            "fees_paid": self.fees_paid,
            "slippage_paid": self.slippage_paid,
            "gross_pnl": self.gross_pnl,
            "net_pnl": self.net_pnl,
            "expected_time_delta": self.expected_time_delta,
            "detected_gap_count": self.detected_gap_count,
            "max_gap_multiple": self.max_gap_multiple,
            "crosses_gap": self.crosses_gap,
        }


@dataclass(frozen=True)
class SimulationResult:
    simulation_id: str
    package_id: str
    strategy_id: str
    strategy_version: str
    snapshot_id: str
    simulation_status: SimulationStatus
    output_scope: str
    simulation_reason: str
    starting_capital: float
    ending_capital: float
    equity_curve: tuple[dict[str, Any], ...]
    trades: tuple[TradeRecord, ...]
    total_trade_count: int
    total_winning_trades: int
    total_losing_trades: int
    total_breakeven_trades: int
    assumptions_reference: str
    governance_reference: str
    temporal_reference: str

    def __post_init__(self) -> None:
        if not isinstance(self.simulation_status, SimulationStatus):
            raise TypeError("simulation_status must be a SimulationStatus")

    def to_dict(self) -> dict[str, Any]:
        return {
            "simulation_id": self.simulation_id,
            "package_id": self.package_id,
            "strategy_id": self.strategy_id,
            "strategy_version": self.strategy_version,
            "snapshot_id": self.snapshot_id,
            "simulation_status": self.simulation_status.value,
            "output_scope": self.output_scope,
            "simulation_reason": self.simulation_reason,
            "starting_capital": self.starting_capital,
            "ending_capital": self.ending_capital,
            "equity_curve": list(self.equity_curve),
            "trades": [trade.to_dict() for trade in self.trades],
            "total_trade_count": self.total_trade_count,
            "total_winning_trades": self.total_winning_trades,
            "total_losing_trades": self.total_losing_trades,
            "total_breakeven_trades": self.total_breakeven_trades,
            "assumptions_reference": self.assumptions_reference,
            "governance_reference": self.governance_reference,
            "temporal_reference": self.temporal_reference,
        }


class GapAwareSimulationCore:
    """Run deterministic long-only raw simulation over declared package series."""

    def __init__(
        self,
        adapted_package: AdaptedBacktestPackage,
        temporal_result: TemporalAdmissibilityResult,
        governance_result: GovernanceGateResult,
        assumptions: ExecutionAssumptionSet,
    ) -> None:
        self.adapted_package = adapted_package
        self.temporal_result = temporal_result
        self.governance_result = governance_result
        self.assumptions = assumptions

    def run(self) -> SimulationResult:
        failures, missing = _validate_inputs(
            self.adapted_package,
            self.temporal_result,
            self.governance_result,
            self.assumptions,
        )
        if missing:
            return _rejected_result(
                self.adapted_package,
                self.temporal_result,
                self.governance_result,
                self.assumptions,
                SimulationStatus.INSUFFICIENT_INFORMATION,
                "Simulation cannot run because required input information is missing: "
                + "; ".join(missing),
            )
        if failures:
            return _rejected_result(
                self.adapted_package,
                self.temporal_result,
                self.governance_result,
                self.assumptions,
                SimulationStatus.REJECTED,
                "Simulation rejected by upstream governance or assumption validation: "
                + "; ".join(failures),
            )

        trades: list[TradeRecord] = []
        equity = self.assumptions.starting_capital
        equity_curve: list[dict[str, Any]] = []

        for key, series in sorted(self.adapted_package.series.items()):
            frame = _load_declared_series_frame(series.parquet_path)
            executable = _prepare_executable_rows(frame, series.symbol, series.timeframe)
            if len(executable) < 3:
                continue
            gap_metadata = _detect_gap_metadata(executable, series.timeframe)
            trade = _simulate_one_long_trade(
                package_id=self.adapted_package.adapted_package_id,
                symbol=series.symbol,
                timeframe=series.timeframe,
                executable=executable,
                assumptions=self.assumptions,
                current_equity=equity,
                gap_metadata=gap_metadata,
            )
            trades.append(trade)
            equity += trade.net_pnl
            equity_curve.append(
                {
                    "timestamp": trade.exit_timestamp.isoformat(),
                    "equity": equity,
                    "position_state": PositionState.FLAT.value,
                    "symbol": series.symbol,
                    "timeframe": series.timeframe,
                }
            )

        if not trades:
            return _rejected_result(
                self.adapted_package,
                self.temporal_result,
                self.governance_result,
                self.assumptions,
                SimulationStatus.INSUFFICIENT_INFORMATION_NO_EXECUTABLE_SERIES,
                "Raw execution scaffold has no executable series with at least three "
                "available rows. No bars were fabricated, interpolated, or forward-filled.",
            )

        winning_trades = sum(1 for trade in trades if trade.net_pnl > 0)
        losing_trades = sum(1 for trade in trades if trade.net_pnl < 0)
        breakeven_trades = sum(1 for trade in trades if trade.net_pnl == 0)
        return SimulationResult(
            simulation_id=_deterministic_simulation_id(
                self.adapted_package,
                self.temporal_result,
                self.governance_result,
                self.assumptions,
            ),
            package_id=self.adapted_package.adapted_package_id,
            strategy_id=self.adapted_package.strategy_id,
            strategy_version=self.adapted_package.strategy_version,
            snapshot_id=self.adapted_package.snapshot_id,
            simulation_status=SimulationStatus.COMPLETED_RAW_EXECUTION,
            output_scope="raw_execution_scaffold",
            simulation_reason=(
                "Raw execution scaffold completed. This is infrastructure execution "
                "plumbing only: not strategy validation, not performance evidence, "
                "not confidence evidence, and not Stage 09 readiness."
            ),
            starting_capital=self.assumptions.starting_capital,
            ending_capital=equity,
            equity_curve=tuple(equity_curve),
            trades=tuple(trades),
            total_trade_count=len(trades),
            total_winning_trades=winning_trades,
            total_losing_trades=losing_trades,
            total_breakeven_trades=breakeven_trades,
            assumptions_reference=self.assumptions.assumption_set_id,
            governance_reference=self.governance_result.package_id,
            temporal_reference=self.temporal_result.package_id,
        )


def run_gap_aware_simulation(
    adapted_package: AdaptedBacktestPackage,
    temporal_result: TemporalAdmissibilityResult,
    governance_result: GovernanceGateResult,
    assumptions: ExecutionAssumptionSet,
) -> SimulationResult:
    return GapAwareSimulationCore(
        adapted_package,
        temporal_result,
        governance_result,
        assumptions,
    ).run()


def _validate_inputs(
    package: AdaptedBacktestPackage,
    temporal: TemporalAdmissibilityResult,
    governance: GovernanceGateResult,
    assumptions: ExecutionAssumptionSet,
) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    missing: list[str] = []
    validate_execution_assumption_set(assumptions)

    if temporal.certification_status is TemporalAdmissibilityStatus.REJECTED:
        failures.append("temporal result is rejected")
    elif (
        temporal.certification_status
        is TemporalAdmissibilityStatus.INSUFFICIENT_INFORMATION
    ):
        missing.append("temporal result has insufficient information")
    elif temporal.certification_status is not TemporalAdmissibilityStatus.CERTIFIED:
        failures.append("temporal result is not certified")
    if temporal.admissible is not True:
        failures.append("temporal result must be admissible")
    if governance.gate_status is GovernanceGateStatus.REJECTED:
        failures.append("governance gate is rejected")
    elif governance.gate_status is GovernanceGateStatus.INSUFFICIENT_INFORMATION:
        missing.append("governance gate has insufficient information")
    elif governance.gate_status is not GovernanceGateStatus.PASSED:
        failures.append("governance gate is not passed")
    if assumptions.governance_gate_status is not GovernanceGateStatus.PASSED:
        failures.append("assumptions must reference a passed governance gate")
    if assumptions.order_execution_timing is OrderExecutionTiming.SAME_BAR_CLOSE_FORBIDDEN:
        failures.append("same-bar execution is forbidden")
    if assumptions.order_execution_timing is not OrderExecutionTiming.NEXT_BAR_OPEN:
        failures.append("only next_bar_open execution is supported")
    if assumptions.allow_short is True:
        failures.append("short execution is not supported by Block 09")

    expected_package_id = package.adapted_package_id
    identity_values = (
        (temporal.package_id, "temporal package_id"),
        (governance.package_id, "governance package_id"),
        (assumptions.created_for_package_id, "assumptions package_id"),
    )
    for actual, label in identity_values:
        if actual != expected_package_id:
            failures.append(f"{label} must match adapted package")
    if temporal.strategy_id != package.strategy_id:
        failures.append("temporal strategy_id must match adapted package")
    if temporal.strategy_version != package.strategy_version:
        failures.append("temporal strategy_version must match adapted package")
    if temporal.snapshot_id != package.snapshot_id:
        failures.append("temporal snapshot_id must match adapted package")
    if governance.strategy_id != package.strategy_id:
        failures.append("governance strategy_id must match adapted package")
    if governance.strategy_version != package.strategy_version:
        failures.append("governance strategy_version must match adapted package")
    if governance.snapshot_id != package.snapshot_id:
        failures.append("governance snapshot_id must match adapted package")
    if assumptions.created_for_strategy_id != package.strategy_id:
        failures.append("assumptions strategy_id must match adapted package")
    if assumptions.created_for_snapshot_id != package.snapshot_id:
        failures.append("assumptions snapshot_id must match adapted package")
    if not package.series:
        missing.append("adapted package must contain at least one series")
    return failures, missing


def _load_declared_series_frame(parquet_path: Path) -> pd.DataFrame:
    if not isinstance(parquet_path, Path) or not parquet_path.is_file():
        raise FileNotFoundError(f"declared parquet file does not exist: {parquet_path}")
    return pd.read_parquet(parquet_path)


def _prepare_executable_rows(
    frame: pd.DataFrame,
    symbol: str,
    timeframe: str,
) -> pd.DataFrame:
    required_columns = {"timestamp", "symbol", "timeframe", "open"}
    missing_columns = required_columns.difference(frame.columns)
    if missing_columns:
        raise ValueError(f"series missing executable columns: {sorted(missing_columns)}")
    filtered = frame.loc[
        (frame["symbol"].astype(str) == symbol)
        & (frame["timeframe"].astype(str) == timeframe),
        ["timestamp", "open"],
    ].copy()
    filtered["timestamp"] = pd.to_datetime(filtered["timestamp"], utc=True, errors="coerce")
    filtered["open"] = pd.to_numeric(filtered["open"], errors="coerce")
    filtered = filtered.dropna(subset=["timestamp", "open"])
    filtered = filtered.sort_values("timestamp", kind="mergesort")
    return filtered


def _simulate_one_long_trade(
    *,
    package_id: str,
    symbol: str,
    timeframe: str,
    executable: pd.DataFrame,
    assumptions: ExecutionAssumptionSet,
    current_equity: float,
    gap_metadata: dict[str, Any],
) -> TradeRecord:
    entry_row = executable.iloc[1]
    exit_row = executable.iloc[2]
    raw_entry = float(entry_row["open"])
    raw_exit = float(exit_row["open"])
    entry_timestamp = _to_datetime(entry_row["timestamp"])
    exit_timestamp = _to_datetime(exit_row["timestamp"])
    slippage_rate = _slippage_bps(assumptions) / 10_000
    fee_rate = _fee_bps(assumptions) / 10_000

    entry_price = raw_entry * (1 + slippage_rate)
    exit_price = raw_exit * (1 - slippage_rate)
    notional = current_equity * assumptions.max_position_fraction
    quantity = notional / entry_price
    entry_notional = entry_price * quantity
    exit_notional = exit_price * quantity
    fees_paid = (entry_notional + exit_notional) * fee_rate
    slippage_paid = abs(entry_price - raw_entry) * quantity + abs(raw_exit - exit_price) * quantity
    gross_pnl = (raw_exit - raw_entry) * quantity
    net_pnl = (exit_price - entry_price) * quantity - fees_paid

    return TradeRecord(
        trade_id=_deterministic_trade_id(package_id, symbol, timeframe, entry_timestamp),
        symbol=symbol,
        timeframe=timeframe,
        entry_timestamp=entry_timestamp,
        exit_timestamp=exit_timestamp,
        entry_price=entry_price,
        exit_price=exit_price,
        quantity=quantity,
        direction=PositionState.LONG,
        fees_paid=fees_paid,
        slippage_paid=slippage_paid,
        gross_pnl=gross_pnl,
        net_pnl=net_pnl,
        expected_time_delta=gap_metadata["expected_time_delta"],
        detected_gap_count=gap_metadata["detected_gap_count"],
        max_gap_multiple=gap_metadata["max_gap_multiple"],
        crosses_gap=gap_metadata["crosses_gap"],
    )


def _fee_bps(assumptions: ExecutionAssumptionSet) -> float:
    if assumptions.fee_model_type is FeeModelType.ZERO_FEE_FOR_DRY_RUN_ONLY:
        return 0.0
    if assumptions.fee_model_type is FeeModelType.FLAT_BPS:
        return assumptions.flat_fee_bps
    return assumptions.taker_fee_bps


def _slippage_bps(assumptions: ExecutionAssumptionSet) -> float:
    if assumptions.slippage_model_type is SlippageModelType.ZERO_SLIPPAGE_FOR_DRY_RUN_ONLY:
        return 0.0
    return assumptions.slippage_bps


def _to_datetime(value: Any) -> datetime:
    if isinstance(value, pd.Timestamp):
        value = value.to_pydatetime()
    if not isinstance(value, datetime):
        raise TypeError("timestamp must be datetime-like")
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def _rejected_result(
    package: AdaptedBacktestPackage,
    temporal: TemporalAdmissibilityResult,
    governance: GovernanceGateResult,
    assumptions: ExecutionAssumptionSet,
    status: SimulationStatus,
    reason: str,
) -> SimulationResult:
    return SimulationResult(
        simulation_id=_deterministic_simulation_id(package, temporal, governance, assumptions),
        package_id=package.adapted_package_id,
        strategy_id=package.strategy_id,
        strategy_version=package.strategy_version,
        snapshot_id=package.snapshot_id,
        simulation_status=status,
        output_scope="raw_execution_scaffold",
        simulation_reason=reason,
        starting_capital=assumptions.starting_capital,
        ending_capital=assumptions.starting_capital,
        equity_curve=(),
        trades=(),
        total_trade_count=0,
        total_winning_trades=0,
        total_losing_trades=0,
        total_breakeven_trades=0,
        assumptions_reference=assumptions.assumption_set_id,
        governance_reference=governance.package_id,
        temporal_reference=temporal.package_id,
    )


def _deterministic_simulation_id(
    package: AdaptedBacktestPackage,
    temporal: TemporalAdmissibilityResult,
    governance: GovernanceGateResult,
    assumptions: ExecutionAssumptionSet,
) -> str:
    payload = {
        "package_id": package.adapted_package_id,
        "strategy_id": package.strategy_id,
        "strategy_version": package.strategy_version,
        "snapshot_id": package.snapshot_id,
        "temporal_reference": temporal.package_id,
        "governance_reference": governance.package_id,
        "assumptions_reference": assumptions.assumption_set_id,
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return f"raw-simulation-{digest[:16]}"


def _deterministic_trade_id(
    package_id: str,
    symbol: str,
    timeframe: str,
    entry_timestamp: datetime,
) -> str:
    payload = {
        "package_id": package_id,
        "symbol": symbol,
        "timeframe": timeframe,
        "entry_timestamp": entry_timestamp.isoformat(),
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return f"trade-{digest[:16]}"


def _detect_gap_metadata(
    executable: pd.DataFrame,
    timeframe: str,
) -> dict[str, Any]:
    expected_delta = _expected_time_delta(timeframe)
    if expected_delta is None or len(executable) < 2:
        return {
            "expected_time_delta": None,
            "detected_gap_count": 0,
            "max_gap_multiple": 0.0,
            "crosses_gap": False,
        }

    timestamps = [_to_datetime(value) for value in executable["timestamp"].tolist()]
    gap_multiples: list[float] = []
    for earlier, later in zip(timestamps, timestamps[1:], strict=False):
        actual_delta = later - earlier
        multiple = actual_delta / expected_delta
        gap_multiples.append(float(multiple))

    detected_gap_count = sum(1 for multiple in gap_multiples if multiple > 1.0)
    entry_exit_multiple = gap_multiples[1] if len(gap_multiples) > 1 else 0.0
    return {
        "expected_time_delta": str(expected_delta),
        "detected_gap_count": detected_gap_count,
        "max_gap_multiple": max(gap_multiples, default=0.0),
        "crosses_gap": entry_exit_multiple > 1.0,
    }


def _expected_time_delta(timeframe: str):
    if timeframe == "1d":
        return pd.Timedelta(days=1)
    if timeframe == "4h":
        return pd.Timedelta(hours=4)
    return None
