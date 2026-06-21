"""Structural adapters for 06 Backtesting Engine."""

from adapters.strategy_dossier_adapter import (
    AdaptedBacktestPackage,
    AdaptedGovernanceState,
    AdaptedSeriesReference,
    StrategyDossierAdapter,
    adapt_strategy_dossier,
)

__all__ = [
    "AdaptedBacktestPackage",
    "AdaptedGovernanceState",
    "AdaptedSeriesReference",
    "StrategyDossierAdapter",
    "adapt_strategy_dossier",
]
