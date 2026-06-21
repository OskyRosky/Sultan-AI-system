"""Raw deterministic simulation core for 06 Backtesting Engine."""

from simulation.gap_aware_simulation_core import (
    GapAwareSimulationCore,
    PositionState,
    SimulationResult,
    SimulationStatus,
    TradeRecord,
    run_gap_aware_simulation,
)

__all__ = [
    "GapAwareSimulationCore",
    "PositionState",
    "SimulationResult",
    "SimulationStatus",
    "TradeRecord",
    "run_gap_aware_simulation",
]
