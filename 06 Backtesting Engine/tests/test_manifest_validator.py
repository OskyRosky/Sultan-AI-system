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
