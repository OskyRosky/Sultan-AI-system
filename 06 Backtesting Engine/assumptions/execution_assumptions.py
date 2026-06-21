"""Non-empirical execution, friction, and position assumptions for 06B.

These models are deterministic assumption records for later simulation blocks.
They do not load data, calculate returns, create signals or labels, generate
trades, compute metrics or PnL, run backtests, or produce empirical evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import re
from typing import Any, Sequence

from governance.pre_execution_governance_gate import (
    GovernanceGateResult,
    GovernanceGateStatus,
)


SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
MAX_LEVERAGE_BOUND = 10.0


class FeeModelType(str, Enum):
    MAKER_TAKER = "maker_taker"
    FLAT_BPS = "flat_bps"
    ZERO_FEE_FOR_DRY_RUN_ONLY = "zero_fee_for_dry_run_only"


class SlippageModelType(str, Enum):
    FIXED_BPS = "fixed_bps"
    PERCENTAGE_OF_SPREAD = "percentage_of_spread"
    ZERO_SLIPPAGE_FOR_DRY_RUN_ONLY = "zero_slippage_for_dry_run_only"


class OrderExecutionTiming(str, Enum):
    NEXT_BAR_OPEN = "next_bar_open"
    NEXT_BAR_CLOSE = "next_bar_close"
    SAME_BAR_CLOSE_FORBIDDEN = "same_bar_close_forbidden"


class PositionSizingMode(str, Enum):
    FIXED_NOTIONAL = "fixed_notional"
    FIXED_FRACTIONAL_EQUITY = "fixed_fractional_equity"
    DRY_RUN_NO_POSITION_SIZING = "dry_run_no_position_sizing"


@dataclass(frozen=True)
class ExecutionAssumptionSet:
    assumption_set_id: str
    assumption_version: str
    fee_model_type: FeeModelType
    slippage_model_type: SlippageModelType
    order_execution_timing: OrderExecutionTiming
    position_sizing_mode: PositionSizingMode
    maker_fee_bps: float
    taker_fee_bps: float
    flat_fee_bps: float
    slippage_bps: float
    max_position_fraction: float
    starting_capital: float
    currency: str
    allow_short: bool
    allow_leverage: bool
    max_leverage: float
    created_for_package_id: str
    created_for_strategy_id: str
    created_for_snapshot_id: str
    governance_gate_status: GovernanceGateStatus
    non_empirical_scope_statement: str
    forbidden_usage: tuple[str, ...]
    warnings: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        validate_execution_assumption_set(self)

    def to_dict(self) -> dict[str, Any]:
        return {
            "assumption_set_id": self.assumption_set_id,
            "assumption_version": self.assumption_version,
            "fee_model_type": self.fee_model_type.value,
            "slippage_model_type": self.slippage_model_type.value,
            "order_execution_timing": self.order_execution_timing.value,
            "position_sizing_mode": self.position_sizing_mode.value,
            "maker_fee_bps": self.maker_fee_bps,
            "taker_fee_bps": self.taker_fee_bps,
            "flat_fee_bps": self.flat_fee_bps,
            "slippage_bps": self.slippage_bps,
            "max_position_fraction": self.max_position_fraction,
            "starting_capital": self.starting_capital,
            "currency": self.currency,
            "allow_short": self.allow_short,
            "allow_leverage": self.allow_leverage,
            "max_leverage": self.max_leverage,
            "created_for_package_id": self.created_for_package_id,
            "created_for_strategy_id": self.created_for_strategy_id,
            "created_for_snapshot_id": self.created_for_snapshot_id,
            "governance_gate_status": self.governance_gate_status.value,
            "non_empirical_scope_statement": self.non_empirical_scope_statement,
            "forbidden_usage": list(self.forbidden_usage),
            "warnings": list(self.warnings),
        }


def create_default_dry_run_execution_assumptions(
    governance_gate_result: GovernanceGateResult,
) -> ExecutionAssumptionSet:
    """Create deterministic dry-run assumptions from a passed governance gate."""

    if governance_gate_result.gate_status is not GovernanceGateStatus.PASSED:
        raise ValueError("governance_gate_status must be passed")

    return ExecutionAssumptionSet(
        assumption_set_id=_deterministic_assumption_set_id(governance_gate_result),
        assumption_version="1.0.0",
        fee_model_type=FeeModelType.ZERO_FEE_FOR_DRY_RUN_ONLY,
        slippage_model_type=SlippageModelType.ZERO_SLIPPAGE_FOR_DRY_RUN_ONLY,
        order_execution_timing=OrderExecutionTiming.NEXT_BAR_OPEN,
        position_sizing_mode=PositionSizingMode.DRY_RUN_NO_POSITION_SIZING,
        maker_fee_bps=0.0,
        taker_fee_bps=0.0,
        flat_fee_bps=0.0,
        slippage_bps=0.0,
        max_position_fraction=1.0,
        starting_capital=100_000.0,
        currency="USD",
        allow_short=False,
        allow_leverage=False,
        max_leverage=1.0,
        created_for_package_id=governance_gate_result.package_id,
        created_for_strategy_id=governance_gate_result.strategy_id,
        created_for_snapshot_id=governance_gate_result.snapshot_id,
        governance_gate_status=governance_gate_result.gate_status,
        non_empirical_scope_statement=(
            "Dry-run execution assumptions are metadata only. They do not simulate "
            "orders, trades, fills, returns, metrics, PnL, or empirical evidence."
        ),
        forbidden_usage=(
            "paper_trading",
            "live_trading",
            "capital_allocation",
            "strategy_promotion",
            "confidence_scoring",
        ),
        warnings=(
            "zero_fee_for_dry_run_only is not a production realism assumption.",
            "zero_slippage_for_dry_run_only is not a production realism assumption.",
            "Dry-run zero assumptions must not be used for paper trading, live trading, "
            "capital allocation, strategy promotion, or confidence scoring.",
        ),
    )


def validate_execution_assumption_set(
    assumptions: ExecutionAssumptionSet,
) -> ExecutionAssumptionSet:
    _require_text(assumptions.assumption_set_id, "assumption_set_id")
    _require_semver(assumptions.assumption_version, "assumption_version")
    _require_text(assumptions.created_for_package_id, "created_for_package_id")
    _require_text(assumptions.created_for_strategy_id, "created_for_strategy_id")
    _require_text(assumptions.created_for_snapshot_id, "created_for_snapshot_id")
    _require_text(assumptions.currency, "currency")
    _require_text(
        assumptions.non_empirical_scope_statement,
        "non_empirical_scope_statement",
    )
    _require_enum(assumptions.fee_model_type, FeeModelType, "fee_model_type")
    _require_enum(
        assumptions.slippage_model_type,
        SlippageModelType,
        "slippage_model_type",
    )
    _require_enum(
        assumptions.order_execution_timing,
        OrderExecutionTiming,
        "order_execution_timing",
    )
    _require_enum(
        assumptions.position_sizing_mode,
        PositionSizingMode,
        "position_sizing_mode",
    )
    _require_enum(
        assumptions.governance_gate_status,
        GovernanceGateStatus,
        "governance_gate_status",
    )

    if assumptions.governance_gate_status is not GovernanceGateStatus.PASSED:
        raise ValueError("governance_gate_status must be passed")
    if (
        assumptions.order_execution_timing
        is OrderExecutionTiming.SAME_BAR_CLOSE_FORBIDDEN
    ):
        raise ValueError("same_bar_close_forbidden cannot be executable timing")
    if min(
        assumptions.maker_fee_bps,
        assumptions.taker_fee_bps,
        assumptions.flat_fee_bps,
    ) < 0:
        raise ValueError("fees cannot be negative")
    if assumptions.slippage_bps < 0:
        raise ValueError("slippage cannot be negative")
    if assumptions.starting_capital <= 0:
        raise ValueError("starting_capital must be positive")
    if not 0 < assumptions.max_position_fraction <= 1:
        raise ValueError("max_position_fraction must be > 0 and <= 1")
    if assumptions.allow_leverage is False and assumptions.max_leverage != 1:
        raise ValueError("allow_leverage false requires max_leverage == 1")
    if assumptions.allow_leverage is True:
        if assumptions.max_leverage <= 1:
            raise ValueError("allow_leverage true requires max_leverage > 1")
        if assumptions.max_leverage > MAX_LEVERAGE_BOUND:
            raise ValueError("max_leverage exceeds bounded dry-run limit")

    _require_forbidden_usage(
        assumptions.forbidden_usage,
        (
            "paper_trading",
            "live_trading",
            "capital_allocation",
            "strategy_promotion",
            "confidence_scoring",
        ),
    )
    _validate_dry_run_warnings(assumptions)
    return assumptions


def _validate_dry_run_warnings(assumptions: ExecutionAssumptionSet) -> None:
    warning_text = " ".join(assumptions.warnings)
    if assumptions.fee_model_type is FeeModelType.ZERO_FEE_FOR_DRY_RUN_ONLY:
        if "zero_fee_for_dry_run_only" not in warning_text:
            raise ValueError("zero_fee_for_dry_run_only requires explicit warning")
    if (
        assumptions.slippage_model_type
        is SlippageModelType.ZERO_SLIPPAGE_FOR_DRY_RUN_ONLY
    ):
        if "zero_slippage_for_dry_run_only" not in warning_text:
            raise ValueError("zero_slippage_for_dry_run_only requires explicit warning")
    if (
        assumptions.fee_model_type is FeeModelType.ZERO_FEE_FOR_DRY_RUN_ONLY
        or assumptions.slippage_model_type
        is SlippageModelType.ZERO_SLIPPAGE_FOR_DRY_RUN_ONLY
    ):
        if "production realism" not in warning_text:
            raise ValueError("dry-run zero assumptions must reject production realism")


def _deterministic_assumption_set_id(
    governance_gate_result: GovernanceGateResult,
) -> str:
    payload = {
        "package_id": governance_gate_result.package_id,
        "strategy_id": governance_gate_result.strategy_id,
        "strategy_version": governance_gate_result.strategy_version,
        "snapshot_id": governance_gate_result.snapshot_id,
        "gate_status": governance_gate_result.gate_status.value,
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return f"exec-assumptions-{digest[:16]}"


def _require_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_semver(value: object, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not SEMVER_PATTERN.fullmatch(text):
        raise ValueError(f"{field_name} must follow SemVer MAJOR.MINOR.PATCH")
    return text


def _require_enum(value: object, enum_type: type[Enum], field_name: str) -> None:
    if not isinstance(value, enum_type):
        raise TypeError(f"{field_name} must be a {enum_type.__name__}")


def _require_forbidden_usage(
    actual: Sequence[str],
    required: Sequence[str],
) -> None:
    missing = [value for value in required if value not in actual]
    if missing:
        raise ValueError(f"forbidden_usage missing required values: {missing}")
