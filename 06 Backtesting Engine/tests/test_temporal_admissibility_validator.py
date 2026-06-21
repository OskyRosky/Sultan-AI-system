from __future__ import annotations

from dataclasses import fields, replace
from datetime import datetime, timedelta, timezone
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
    AdaptedSeriesReference,
    StrategyDossierAdapter,
)
from loaders.feature_snapshot_loader import FeatureSnapshotLoader  # noqa: E402
from mockups.strategy_dossier_mockups import FICTITIOUS_STRATEGY_DOSSIER  # noqa: E402
from packages.input_package_builder import InputPackageBuilder  # noqa: E402
from validators.temporal_admissibility_validator import (  # noqa: E402
    TemporalAdmissibilityResult,
    TemporalAdmissibilityStatus,
    TemporalAdmissibilityValidator,
)


MANIFEST_PATH = REPO_ROOT / (
    "03 Feature Engineering/manifests/"
    "feature_snapshot_technical_v1_1_0_0_20260608_163510.json"
)
SCHEMA_PATH = REPO_ROOT / "03 Feature Engineering/schemas/feature_snapshot_manifest_schema.json"
VALIDATION_TIMESTAMP = datetime(2026, 6, 21, tzinfo=timezone.utc)


def _adapted_package() -> AdaptedBacktestPackage:
    loaded_snapshot = FeatureSnapshotLoader(MANIFEST_PATH, schema_path=SCHEMA_PATH).load()
    input_package = InputPackageBuilder(loaded_snapshot).build()
    return StrategyDossierAdapter(input_package, FICTITIOUS_STRATEGY_DOSSIER).adapt()


def _validate(package: AdaptedBacktestPackage) -> TemporalAdmissibilityResult:
    return TemporalAdmissibilityValidator(
        package,
        validation_timestamp=VALIDATION_TIMESTAMP,
    ).validate()


def test_valid_package_certifies_successfully() -> None:
    result = _validate(_adapted_package())

    assert result.admissible is True
    assert result.certification_status is TemporalAdmissibilityStatus.CERTIFIED
    assert result.certification_scope == "package_metadata_only"
    assert result.blocking_failures == ()
    assert result.temporal_risks == ()


@pytest.mark.parametrize(
    ("field_name", "expected_failure"),
    (
        ("snapshot_id", "snapshot_id must be present"),
        ("feature_version", "feature_version must be present"),
        ("code_commit", "code_commit must be present"),
        ("adapted_package_id", "package_id must be present"),
        ("feature_set", "feature_set must be present"),
        ("strategy_id", "strategy_id must be present"),
        ("strategy_name", "strategy_name must be present"),
        ("strategy_version", "strategy_version must be present"),
        ("warmup_policy", "warmup_policy must be present"),
        ("gap_report_reference", "gap_report_reference must be present"),
        ("quality_report_reference", "quality_report_reference must be present"),
    ),
)
def test_missing_required_text_metadata_is_not_admissible(
    field_name: str,
    expected_failure: str,
) -> None:
    package = replace(_adapted_package(), **{field_name: ""})
    result = _validate(package)

    assert result.admissible is False
    assert result.certification_status is (
        TemporalAdmissibilityStatus.INSUFFICIENT_INFORMATION
    )
    assert expected_failure in result.blocking_failures


def test_missing_manifest_path_rejected() -> None:
    result = _validate(replace(_adapted_package(), manifest_path=Path("missing.json")))

    assert result.admissible is False
    assert result.certification_status is (
        TemporalAdmissibilityStatus.INSUFFICIENT_INFORMATION
    )
    assert "manifest_path must reference an existing file" in result.blocking_failures


def test_missing_schema_path_rejected() -> None:
    result = _validate(replace(_adapted_package(), schema_path=Path("missing.json")))

    assert result.admissible is False
    assert result.certification_status is (
        TemporalAdmissibilityStatus.INSUFFICIENT_INFORMATION
    )
    assert "schema_path must reference an existing file" in result.blocking_failures


def test_empty_warmup_policy_rejected() -> None:
    result = _validate(replace(_adapted_package(), warmup_policy="   "))

    assert result.admissible is False
    assert result.certification_status is (
        TemporalAdmissibilityStatus.INSUFFICIENT_INFORMATION
    )
    assert "warmup_policy must be present" in result.blocking_failures


def test_future_timestamp_rejected() -> None:
    package = _adapted_package()
    first_key = next(iter(package.series))
    first_series = package.series[first_key]
    future_series = replace(
        first_series,
        max_timestamp=datetime(2026, 6, 9, tzinfo=timezone.utc),
    )
    series = dict(package.series)
    series[first_key] = future_series

    result = _validate(replace(package, series=series))

    assert result.admissible is False
    assert result.certification_status is TemporalAdmissibilityStatus.REJECTED
    assert any("future timestamps" in failure for failure in result.blocking_failures)


def test_invalid_temporal_range_rejected() -> None:
    package = _adapted_package()
    first_key = next(iter(package.series))
    first_series = package.series[first_key]
    invalid_series = replace(
        first_series,
        min_timestamp=first_series.max_timestamp + timedelta(days=1),
    )
    series = dict(package.series)
    series[first_key] = invalid_series

    result = _validate(replace(package, series=series))

    assert result.admissible is False
    assert result.certification_status is TemporalAdmissibilityStatus.REJECTED
    assert any("min_timestamp must be <=" in failure for failure in result.blocking_failures)


def test_duplicate_series_rejected() -> None:
    package = _adapted_package()
    first_key = next(iter(package.series))
    first_series = package.series[first_key]
    series = dict(package.series)
    series[("DUPLICATE", "1d")] = first_series

    result = _validate(replace(package, series=series))

    assert result.admissible is False
    assert result.certification_status is TemporalAdmissibilityStatus.REJECTED
    assert any("duplicate symbol/timeframe" in failure for failure in result.blocking_failures)


def test_missing_generated_at_rejected() -> None:
    package = replace(_adapted_package(), generated_at=None)

    result = _validate(package)

    assert result.admissible is False
    assert result.certification_status is (
        TemporalAdmissibilityStatus.INSUFFICIENT_INFORMATION
    )
    assert "generated_at must be present" in result.blocking_failures


def test_generated_at_future_relative_to_validation_timestamp_rejected() -> None:
    package = replace(
        _adapted_package(),
        generated_at=VALIDATION_TIMESTAMP + timedelta(days=1),
    )

    result = _validate(package)

    assert result.admissible is False
    assert result.certification_status is TemporalAdmissibilityStatus.REJECTED
    assert any("generated_at must not be in the future" in failure for failure in result.blocking_failures)


def test_deterministic_validation_output() -> None:
    package = _adapted_package()
    first = _validate(package)
    second = _validate(package)

    assert first == second
    assert first.to_dict() == second.to_dict()


def test_certification_status_enum_enforcement() -> None:
    result = _validate(_adapted_package())

    with pytest.raises(TypeError, match="TemporalAdmissibilityStatus"):
        replace(result, certification_status="certified")


def test_certified_reason_is_explicitly_metadata_only() -> None:
    result = _validate(_adapted_package())
    reason = result.certification_reason

    assert result.certification_scope == "package_metadata_only"
    assert "does not certify feature formulas" in reason
    assert "signal timing" in reason
    assert "execution timing" in reason
    assert "anti-leakage correctness" in reason


def test_block_07_handoff_fields_exist() -> None:
    result = _validate(_adapted_package())

    assert result.handoff_required is True
    assert result.handoff_target == "Block 07"
    assert result.package_id == _adapted_package().adapted_package_id


def test_generated_at_is_propagated_from_loader_to_validator() -> None:
    loaded_snapshot = FeatureSnapshotLoader(MANIFEST_PATH, schema_path=SCHEMA_PATH).load()
    input_package = InputPackageBuilder(loaded_snapshot).build()
    adapted_package = StrategyDossierAdapter(
        input_package,
        FICTITIOUS_STRATEGY_DOSSIER,
    ).adapt()
    result = _validate(adapted_package)

    assert loaded_snapshot.generated_at == input_package.generated_at
    assert input_package.generated_at == adapted_package.generated_at
    assert adapted_package.generated_at == result.generated_at


def test_adapted_governance_temporal_status_remains_not_certified() -> None:
    package = _adapted_package()

    assert package.governance_state.temporal_admissibility_status == (
        "temporal_admissibility_not_certified"
    )
    assert _validate(package).admissible is True
    assert package.governance_state.temporal_admissibility_status == (
        "temporal_admissibility_not_certified"
    )


def test_validator_does_not_mutate_package() -> None:
    package = _adapted_package()
    serialized_before = package.to_dict()
    series_ids_before = {key: id(value) for key, value in package.series.items()}

    _validate(package)

    assert package.to_dict() == serialized_before
    assert {key: id(value) for key, value in package.series.items()} == series_ids_before


def test_validator_does_not_re_read_manifest(monkeypatch: pytest.MonkeyPatch) -> None:
    package = _adapted_package()

    def fail_read_text(*args, **kwargs):
        raise AssertionError("validator must not re-read manifest")

    monkeypatch.setattr(Path, "read_text", fail_read_text)

    assert _validate(package).admissible is True


def test_validator_does_not_load_parquet(monkeypatch: pytest.MonkeyPatch) -> None:
    package = _adapted_package()

    def fail_read_parquet(*args, **kwargs):
        raise AssertionError("validator must not load parquet")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    assert _validate(package).admissible is True


def test_validator_does_not_create_metrics() -> None:
    result = _validate(_adapted_package())
    field_names = {field.name.lower() for field in fields(TemporalAdmissibilityResult)}
    serialized = repr(result.to_dict()).lower()

    assert "metrics" not in field_names
    assert "metrics" not in serialized


def test_validator_does_not_create_trades_signals_labels_or_pnl() -> None:
    result = _validate(_adapted_package())
    field_names = {field.name.lower() for field in fields(TemporalAdmissibilityResult)}
    serialized = repr(result.to_dict()).lower()

    for forbidden in ("trades", "signals", "labels", "pnl"):
        assert forbidden not in field_names
        assert forbidden not in serialized
