from __future__ import annotations

from dataclasses import fields, replace
from datetime import datetime, timedelta, timezone
import json
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


def _manifest_payload() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _write_manifest(tmp_path: Path, payload: dict[str, object]) -> Path:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_valid_package_certifies_successfully() -> None:
    result = _validate(_adapted_package())

    assert result.admissible is True
    assert result.certification_status is TemporalAdmissibilityStatus.CERTIFIED
    assert result.blocking_failures == ()
    assert result.temporal_risks == ()


@pytest.mark.parametrize(
    ("field_name", "expected_failure"),
    (
        ("snapshot_id", "snapshot_id must be present"),
        ("feature_version", "feature_version must be present"),
        ("code_commit", "code_commit must be present"),
        ("strategy_id", "strategy_id must be present"),
        ("warmup_policy", "warmup_policy must be present"),
        ("gap_report_reference", "gap_report_reference must be present"),
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


def test_missing_generated_at_rejected(tmp_path: Path) -> None:
    payload = _manifest_payload()
    del payload["generated_at"]
    package = replace(_adapted_package(), manifest_path=_write_manifest(tmp_path, payload))

    result = _validate(package)

    assert result.admissible is False
    assert result.certification_status is (
        TemporalAdmissibilityStatus.INSUFFICIENT_INFORMATION
    )
    assert "generated_at must be present" in result.blocking_failures


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


def test_validator_does_not_mutate_package() -> None:
    package = _adapted_package()
    serialized_before = package.to_dict()
    series_ids_before = {key: id(value) for key, value in package.series.items()}

    _validate(package)

    assert package.to_dict() == serialized_before
    assert {key: id(value) for key, value in package.series.items()} == series_ids_before


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
