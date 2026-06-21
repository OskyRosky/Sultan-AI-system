from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timezone
from pathlib import Path
import sys

import pandas as pd
import pytest


BACKTESTING_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKTESTING_ROOT.parents[0]
STRATEGY_ENGINE_ROOT = REPO_ROOT / "05 Strategy Engine"
if str(BACKTESTING_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKTESTING_ROOT))
if str(STRATEGY_ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from adapters.strategy_dossier_adapter import (  # noqa: E402
    AdaptedBacktestPackage,
    StrategyDossierAdapter,
)
from assumptions.execution_assumptions import (  # noqa: E402
    FeeModelType,
    OrderExecutionTiming,
    SlippageModelType,
    create_default_dry_run_execution_assumptions,
)
from governance.pre_execution_governance_gate import (  # noqa: E402
    GovernanceGateStatus,
    PreExecutionGovernanceGate,
)
from loaders.feature_snapshot_loader import FeatureSnapshotLoader  # noqa: E402
from mockups.strategy_dossier_mockups import FICTITIOUS_STRATEGY_DOSSIER  # noqa: E402
from packages.input_package_builder import InputPackageBuilder  # noqa: E402
from simulation.gap_aware_simulation_core import (  # noqa: E402
    GapAwareSimulationCore,
    SimulationResult,
    SimulationStatus,
    TradeRecord,
)
from validators.temporal_admissibility_validator import (  # noqa: E402
    TemporalAdmissibilityStatus,
    TemporalAdmissibilityValidator,
)


MANIFEST_PATH = REPO_ROOT / (
    "03 Feature Engineering/manifests/"
    "feature_snapshot_technical_v1_1_0_0_20260608_163510.json"
)
SCHEMA_PATH = REPO_ROOT / "03 Feature Engineering/schemas/feature_snapshot_manifest_schema.json"
VALIDATION_TIMESTAMP = datetime(2026, 6, 21, tzinfo=timezone.utc)


def _upstream_artifacts():
    loaded_snapshot = FeatureSnapshotLoader(MANIFEST_PATH, schema_path=SCHEMA_PATH).load()
    input_package = InputPackageBuilder(loaded_snapshot).build()
    adapted_package = StrategyDossierAdapter(
        input_package,
        FICTITIOUS_STRATEGY_DOSSIER,
    ).adapt()
    temporal_result = TemporalAdmissibilityValidator(
        adapted_package,
        validation_timestamp=VALIDATION_TIMESTAMP,
    ).validate()
    governance_result = PreExecutionGovernanceGate(
        adapted_package,
        temporal_result,
        validation_timestamp=VALIDATION_TIMESTAMP,
    ).evaluate()
    assumptions = create_default_dry_run_execution_assumptions(governance_result)
    return adapted_package, temporal_result, governance_result, assumptions


def _write_series_parquet(
    tmp_path: Path,
    rows: list[dict[str, object]],
    *,
    name: str = "series.parquet",
) -> Path:
    path = tmp_path / name
    pd.DataFrame(rows).to_parquet(path, index=False)
    return path


def _rows(prices: list[float]) -> list[dict[str, object]]:
    base_dates = pd.date_range("2026-01-01", periods=len(prices), freq="D", tz="UTC")
    return [
        {
            "timestamp": timestamp,
            "symbol": "BTCUSDT",
            "timeframe": "1d",
            "open": price,
        }
        for timestamp, price in zip(base_dates, prices, strict=True)
    ]


def _package_with_rows(
    tmp_path: Path,
    rows: list[dict[str, object]],
) -> tuple:
    package, temporal, governance, assumptions = _upstream_artifacts()
    first_key = next(iter(package.series))
    first_series = package.series[first_key]
    parquet_path = _write_series_parquet(tmp_path, rows)
    series = {
        ("BTCUSDT", "1d"): replace(
            first_series,
            symbol="BTCUSDT",
            timeframe="1d",
            row_count=len(rows),
            parquet_path=parquet_path,
        )
    }
    return replace(package, series=series), temporal, governance, assumptions


def _run(package, temporal, governance, assumptions) -> SimulationResult:
    return GapAwareSimulationCore(package, temporal, governance, assumptions).run()


def test_valid_simulation_completes(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(
        tmp_path,
        _rows([100.0, 100.0, 110.0]),
    )

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is SimulationStatus.COMPLETED_RAW_EXECUTION
    assert result.output_scope == "raw_execution_scaffold"
    assert result.total_trade_count == 1
    assert result.ending_capital > result.starting_capital


def test_legacy_completed_status_is_not_emitted_for_success(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(
        tmp_path,
        _rows([100.0, 100.0, 110.0]),
    )

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is not SimulationStatus.COMPLETED
    assert result.simulation_status is SimulationStatus.COMPLETED_RAW_EXECUTION


def test_temporal_rejected_blocks_simulation(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))
    temporal = replace(
        temporal,
        admissible=False,
        certification_status=TemporalAdmissibilityStatus.REJECTED,
    )

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is SimulationStatus.REJECTED
    assert "temporal result is rejected" in result.simulation_reason


def test_temporal_insufficient_information_blocks_simulation_as_insufficient_information(
    tmp_path: Path,
) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))
    temporal = replace(
        temporal,
        admissible=False,
        certification_status=TemporalAdmissibilityStatus.INSUFFICIENT_INFORMATION,
    )

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is SimulationStatus.INSUFFICIENT_INFORMATION
    assert "temporal result has insufficient information" in result.simulation_reason


def test_governance_rejected_blocks_simulation(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))
    governance = replace(governance, gate_status=GovernanceGateStatus.REJECTED)

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is SimulationStatus.REJECTED
    assert "governance gate is rejected" in result.simulation_reason


def test_identity_mismatch_rejected(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))
    assumptions = replace(assumptions, created_for_package_id="other-package")

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is SimulationStatus.REJECTED
    assert "assumptions package_id must match" in result.simulation_reason


def test_governance_strategy_id_mismatch_rejected(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))
    governance = replace(governance, strategy_id="mismatch")

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is SimulationStatus.REJECTED
    assert "governance strategy_id must match adapted package" in result.simulation_reason


def test_assumptions_strategy_id_mismatch_rejected(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))
    assumptions = replace(assumptions, created_for_strategy_id="mismatch")

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is SimulationStatus.REJECTED
    assert "assumptions strategy_id must match adapted package" in result.simulation_reason


@pytest.mark.parametrize(
    ("artifact", "field_name", "expected_error"),
    (
        ("temporal", "strategy_id", "temporal strategy_id must match"),
        ("temporal", "strategy_version", "temporal strategy_version must match"),
        ("temporal", "snapshot_id", "temporal snapshot_id must match"),
        ("governance", "strategy_version", "governance strategy_version must match"),
        ("governance", "snapshot_id", "governance snapshot_id must match"),
        (
            "assumptions",
            "created_for_snapshot_id",
            "assumptions snapshot_id must match",
        ),
    ),
)
def test_cross_input_identity_mismatches_rejected(
    tmp_path: Path,
    artifact: str,
    field_name: str,
    expected_error: str,
) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))
    if artifact == "temporal":
        temporal = replace(temporal, **{field_name: "mismatch"})
    elif artifact == "governance":
        governance = replace(governance, **{field_name: "mismatch"})
    else:
        assumptions = replace(assumptions, **{field_name: "mismatch"})

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is SimulationStatus.REJECTED
    assert expected_error in result.simulation_reason


def test_empty_series_rejected() -> None:
    package, temporal, governance, assumptions = _upstream_artifacts()
    package = replace(package, series={})

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is SimulationStatus.INSUFFICIENT_INFORMATION
    assert "at least one series" in result.simulation_reason


def test_series_with_fewer_than_three_executable_rows_is_insufficient_information(
    tmp_path: Path,
) -> None:
    package, temporal, governance, assumptions = _package_with_rows(
        tmp_path,
        _rows([100.0, 101.0]),
    )

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is (
        SimulationStatus.INSUFFICIENT_INFORMATION_NO_EXECUTABLE_SERIES
    )
    assert "no executable series" in result.simulation_reason
    assert result.total_trade_count == 0


def test_missing_timestamps_handled(tmp_path: Path) -> None:
    rows = _rows([100.0, 100.0, 110.0, 120.0])
    rows[1]["timestamp"] = None
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, rows)

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is SimulationStatus.COMPLETED_RAW_EXECUTION
    assert result.total_trade_count == 1
    assert result.trades[0].entry_timestamp.isoformat().startswith("2026-01-03")


def test_gap_aware_ordering_preserved(tmp_path: Path) -> None:
    rows = _rows([100.0, 110.0, 120.0])
    rows = [rows[2], rows[0], rows[1]]
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, rows)

    result = _run(package, temporal, governance, assumptions)

    assert result.trades[0].entry_timestamp.isoformat().startswith("2026-01-02")
    assert result.trades[0].exit_timestamp.isoformat().startswith("2026-01-03")


def test_same_bar_execution_forbidden(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))

    with pytest.raises(ValueError, match="same_bar_close_forbidden"):
        replace(
            assumptions,
            order_execution_timing=OrderExecutionTiming.SAME_BAR_CLOSE_FORBIDDEN,
        )


def test_next_bar_close_rejected_if_unsupported(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))
    assumptions = replace(
        assumptions,
        order_execution_timing=OrderExecutionTiming.NEXT_BAR_CLOSE,
    )

    result = _run(package, temporal, governance, assumptions)

    assert result.simulation_status is SimulationStatus.REJECTED
    assert "only next_bar_open execution is supported" in result.simulation_reason


def test_fee_application_works(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(
        tmp_path,
        _rows([100.0, 100.0, 110.0]),
    )
    assumptions = replace(
        assumptions,
        fee_model_type=FeeModelType.FLAT_BPS,
        flat_fee_bps=10.0,
        warnings=(*assumptions.warnings, "non-zero flat fee dry-run assumption."),
    )

    result = _run(package, temporal, governance, assumptions)

    assert result.trades[0].fees_paid > 0
    assert result.trades[0].net_pnl < result.trades[0].gross_pnl


def test_slippage_application_works(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(
        tmp_path,
        _rows([100.0, 100.0, 110.0]),
    )
    assumptions = replace(
        assumptions,
        slippage_model_type=SlippageModelType.FIXED_BPS,
        slippage_bps=10.0,
        warnings=(
            *assumptions.warnings,
            "non-zero fixed slippage dry-run assumption.",
        ),
    )

    result = _run(package, temporal, governance, assumptions)

    assert result.trades[0].slippage_paid > 0
    assert result.trades[0].entry_price > 100.0
    assert result.trades[0].exit_price < 110.0


def test_slippage_sizing_does_not_overspend_notional(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(
        tmp_path,
        _rows([100.0, 100.0, 110.0]),
    )
    assumptions = replace(
        assumptions,
        slippage_model_type=SlippageModelType.FIXED_BPS,
        slippage_bps=100.0,
        warnings=(
            *assumptions.warnings,
            "non-zero fixed slippage dry-run assumption.",
        ),
    )

    trade = _run(package, temporal, governance, assumptions).trades[0]

    allowed_notional = assumptions.starting_capital * assumptions.max_position_fraction
    assert trade.entry_price * trade.quantity <= allowed_notional


def test_trade_lifecycle_recorded(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))

    trade = _run(package, temporal, governance, assumptions).trades[0]

    assert trade.trade_id.startswith("trade-")
    assert trade.entry_timestamp < trade.exit_timestamp
    assert trade.quantity > 0


def test_equity_curve_generated(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))

    result = _run(package, temporal, governance, assumptions)

    assert result.equity_curve
    assert result.equity_curve[-1]["equity"] == result.ending_capital


def test_winning_trade_count_correct(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(
        tmp_path,
        _rows([100.0, 100.0, 110.0]),
    )

    result = _run(package, temporal, governance, assumptions)

    assert result.total_winning_trades == 1
    assert result.total_losing_trades == 0
    assert result.total_breakeven_trades == 0


def test_losing_trade_count_correct(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(
        tmp_path,
        _rows([100.0, 100.0, 90.0]),
    )

    result = _run(package, temporal, governance, assumptions)

    assert result.total_winning_trades == 0
    assert result.total_losing_trades == 1
    assert result.total_breakeven_trades == 0


def test_breakeven_trade_accounting(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(
        tmp_path,
        _rows([100.0, 100.0, 100.0]),
    )

    result = _run(package, temporal, governance, assumptions)

    assert result.total_winning_trades == 0
    assert result.total_losing_trades == 0
    assert result.total_breakeven_trades == 1


def test_trade_outcome_counts_sum_to_total_trade_count(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(
        tmp_path,
        _rows([100.0, 100.0, 110.0]),
    )

    result = _run(package, temporal, governance, assumptions)

    assert (
        result.total_winning_trades
        + result.total_losing_trades
        + result.total_breakeven_trades
        == result.total_trade_count
    )


def test_minimal_gap_metadata_detects_gap_between_entry_and_exit(tmp_path: Path) -> None:
    rows = _rows([100.0, 100.0, 110.0])
    rows[2]["timestamp"] = pd.Timestamp("2026-01-05", tz="UTC")
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, rows)

    trade = _run(package, temporal, governance, assumptions).trades[0]

    assert trade.expected_time_delta == "1 days 00:00:00"
    assert trade.detected_gap_count == 1
    assert trade.max_gap_multiple == 3.0
    assert trade.crosses_gap is True


def test_result_declares_raw_execution_scaffold_not_strategy_validation(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(
        tmp_path,
        _rows([100.0, 100.0, 110.0]),
    )

    result = _run(package, temporal, governance, assumptions)

    assert result.output_scope == "raw_execution_scaffold"
    assert "not strategy validation" in result.simulation_reason
    assert "not performance evidence" in result.simulation_reason
    assert "not confidence evidence" in result.simulation_reason
    assert "not Stage 09 readiness" in result.simulation_reason


def test_deterministic_output(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(
        tmp_path,
        _rows([100.0, 100.0, 110.0]),
    )

    first = _run(package, temporal, governance, assumptions)
    second = _run(package, temporal, governance, assumptions)

    assert first == second
    assert first.to_dict() == second.to_dict()


def test_frozen_dataclass_enforcement(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))
    result = _run(package, temporal, governance, assumptions)

    with pytest.raises(FrozenInstanceError):
        result.simulation_status = SimulationStatus.REJECTED


def test_no_mutation_of_inputs(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))
    package_before = package.to_dict()
    temporal_before = temporal.to_dict()
    governance_before = governance.to_dict()
    assumptions_before = assumptions.to_dict()

    _run(package, temporal, governance, assumptions)

    assert package.to_dict() == package_before
    assert temporal.to_dict() == temporal_before
    assert governance.to_dict() == governance_before
    assert assumptions.to_dict() == assumptions_before


def test_no_randomness_in_core_source() -> None:
    source = (BACKTESTING_ROOT / "simulation/gap_aware_simulation_core.py").read_text(
        encoding="utf-8"
    )

    assert "random" not in source.lower()
    assert "monte" not in source.lower()


@pytest.mark.parametrize(
    "forbidden",
    (
        "sharpe",
        "sortino",
        "calmar",
        "oos",
        "walk_forward",
        "robustness",
        "optimization",
        "alpha",
        "beta",
        "cagr",
    ),
)
def test_forbidden_analysis_terms_not_in_result_fields(
    tmp_path: Path,
    forbidden: str,
) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))
    result = _run(package, temporal, governance, assumptions)
    result_fields = {field.name.lower() for field in fields(SimulationResult)}
    trade_fields = {field.name.lower() for field in fields(TradeRecord)}

    assert forbidden not in result_fields
    assert forbidden not in trade_fields
    assert forbidden not in repr(result.to_dict()).lower()


def test_no_stage_09_readiness_change(tmp_path: Path) -> None:
    package, temporal, governance, assumptions = _package_with_rows(tmp_path, _rows([1, 2, 3]))

    _run(package, temporal, governance, assumptions)

    assert package.governance_state.stage_09_readiness == "blocked"
    assert package.governance_state.handoff_to_09 == "blocked"
