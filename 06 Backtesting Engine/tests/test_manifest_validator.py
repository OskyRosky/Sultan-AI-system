from __future__ import annotations

import copy
import json
from pathlib import Path
import sys

import pytest


BACKTESTING_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKTESTING_ROOT.parents[0]
if str(BACKTESTING_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKTESTING_ROOT))

from loaders.manifest_validator import validate_feature_snapshot_manifest  # noqa: E402


MANIFEST_PATH = REPO_ROOT / (
    "03 Feature Engineering/manifests/"
    "feature_snapshot_technical_v1_1_0_0_20260608_163510.json"
)
SCHEMA_PATH = REPO_ROOT / "03 Feature Engineering/schemas/feature_snapshot_manifest_schema.json"


def _manifest_payload() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _write_manifest(tmp_path: Path, payload: dict[str, object]) -> Path:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _validate_payload(tmp_path: Path, payload: dict[str, object]):
    return validate_feature_snapshot_manifest(
        _write_manifest(tmp_path, payload),
        schema_path=SCHEMA_PATH,
    )


def _first_series(payload: dict[str, object]) -> dict[str, object]:
    series = copy.deepcopy(payload["series"])
    payload["series"] = series
    return series[0]


def test_valid_official_manifest_passes() -> None:
    result = validate_feature_snapshot_manifest(MANIFEST_PATH, schema_path=SCHEMA_PATH)

    assert result.passed is True
    assert result.errors == ()
    assert result.manifest is not None
    assert result.manifest.lineage.snapshot_id == (
        "feature_snapshot_technical_v1_1_0_0_20260608_163510"
    )
    assert result.manifest.symbols == ("BTCUSDT", "ETHUSDT")
    assert result.manifest.timeframes == ("1d", "4h")
    assert result.manifest_path == MANIFEST_PATH
    assert result.schema_path == SCHEMA_PATH


def test_missing_required_field_fails_schema_validation(tmp_path: Path) -> None:
    payload = _manifest_payload()
    del payload["snapshot_id"]

    result = validate_feature_snapshot_manifest(
        _write_manifest(tmp_path, payload),
        schema_path=SCHEMA_PATH,
    )

    assert result.passed is False
    assert result.manifest is None
    assert any("snapshot_id" in error for error in result.errors)


def test_invalid_feature_version_fails_metadata_validation(tmp_path: Path) -> None:
    payload = _manifest_payload()
    payload["feature_version"] = "v1"

    result = validate_feature_snapshot_manifest(
        _write_manifest(tmp_path, payload),
        schema_path=SCHEMA_PATH,
    )

    assert result.passed is False
    assert result.errors == ("feature_version must follow SemVer MAJOR.MINOR.PATCH",)
    assert result.manifest_path == tmp_path / "manifest.json"
    assert result.schema_path == SCHEMA_PATH


def test_missing_parquet_reference_fails_metadata_validation(tmp_path: Path) -> None:
    payload = _manifest_payload()
    series = copy.deepcopy(payload["series"])
    series[0]["parquet_paths"] = []
    payload["series"] = series

    result = validate_feature_snapshot_manifest(
        _write_manifest(tmp_path, payload),
        schema_path=SCHEMA_PATH,
    )

    assert result.passed is False
    assert result.errors == ("series.parquet_paths must contain at least one item",)


def test_schema_mismatch_fails_schema_validation(tmp_path: Path) -> None:
    payload = _manifest_payload()
    payload["unexpected_field"] = "not allowed"

    result = validate_feature_snapshot_manifest(
        _write_manifest(tmp_path, payload),
        schema_path=SCHEMA_PATH,
    )

    assert result.passed is False
    assert result.manifest is None
    assert any("Additional properties are not allowed" in error for error in result.errors)


@pytest.mark.parametrize(
    ("field_name", "value", "expected_error"),
    (
        ("ready_for_backtesting", False, "ready_for_backtesting must be true"),
        ("status", "partial", "manifest status must be complete"),
    ),
)
def test_lineage_blocking_statuses_fail(
    tmp_path: Path,
    field_name: str,
    value: object,
    expected_error: str,
) -> None:
    payload = _manifest_payload()
    payload[field_name] = value

    result = _validate_payload(tmp_path, payload)

    assert result.passed is False
    assert result.errors == (expected_error + " for 06 consumption",)


@pytest.mark.parametrize(
    ("field_name", "value", "expected_error"),
    (
        (
            "min_timestamp",
            "2026-06-08T00:00:00+00:00",
            "series min_timestamp must be <= max_timestamp",
        ),
        ("row_count", 0, "series row_count must be positive"),
        (
            "data_quality_score",
            -0.1,
            "data_quality_score",
        ),
        (
            "data_quality_score",
            1.1,
            "data_quality_score",
        ),
    ),
)
def test_invalid_series_metadata_fails(
    tmp_path: Path,
    field_name: str,
    value: object,
    expected_error: str,
) -> None:
    payload = _manifest_payload()
    series = _first_series(payload)
    series[field_name] = value
    if field_name == "min_timestamp":
        series["max_timestamp"] = "2026-06-07T00:00:00+00:00"

    result = _validate_payload(tmp_path, payload)

    assert result.passed is False
    assert any(expected_error in error for error in result.errors)


@pytest.mark.parametrize(
    ("parquet_path", "expected_error"),
    (
        (
            "/data/features/technical_v1/1.0.0/BTCUSDT/1d/features_run.parquet",
            "parquet paths must be repository-relative",
        ),
        (
            "data/features/technical_v1/1.0.0/BTCUSDT/features_5faf4e40-0087-4a63-95fe-03e9d11a3271.parquet",
            "parquet path missing expected lineage parts",
        ),
        (
            "data/features/technical_v1/1.0.0/BTCUSDT/1d/features_other-run.parquet",
            "parquet filename must include series run_id",
        ),
        (
            "data/features/technical_v1/1.0.0/BTCUSDT/1d/features_5faf4e40-0087-4a63-95fe-03e9d11a3271.csv",
            "parquet paths must end with .parquet",
        ),
    ),
)
def test_invalid_parquet_references_fail(
    tmp_path: Path,
    parquet_path: str,
    expected_error: str,
) -> None:
    payload = _manifest_payload()
    series = _first_series(payload)
    series["parquet_paths"] = [parquet_path]

    result = _validate_payload(tmp_path, payload)

    assert result.passed is False
    assert any(expected_error in error for error in result.errors)


def test_incomplete_symbol_timeframe_coverage_fails(tmp_path: Path) -> None:
    payload = _manifest_payload()
    payload["series"] = copy.deepcopy(payload["series"])[:-1]

    result = _validate_payload(tmp_path, payload)

    assert result.passed is False
    assert result.errors == ("series must cover every declared symbol/timeframe pair exactly",)


@pytest.mark.parametrize(
    ("field_name", "expected_error"),
    (
        ("symbols", "symbols must not contain duplicates"),
        ("timeframes", "timeframes must not contain duplicates"),
    ),
)
def test_duplicate_symbols_or_timeframes_fail(
    tmp_path: Path,
    field_name: str,
    expected_error: str,
) -> None:
    payload = _manifest_payload()
    values = copy.deepcopy(payload[field_name])
    values.append(values[0])
    payload[field_name] = values

    result = _validate_payload(tmp_path, payload)

    assert result.passed is False
    assert result.errors == (expected_error,)
