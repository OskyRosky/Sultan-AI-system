from __future__ import annotations

import copy
from dataclasses import fields
import json
from pathlib import Path
import shutil
import sys

import pandas as pd
import pytest


BACKTESTING_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKTESTING_ROOT.parents[0]
if str(BACKTESTING_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKTESTING_ROOT))

from loaders.feature_snapshot_loader import (  # noqa: E402
    FeatureSnapshotLoader,
    LoadedFeatureSeries,
    LoadedFeatureSnapshot,
)


MANIFEST_PATH = REPO_ROOT / (
    "03 Feature Engineering/manifests/"
    "feature_snapshot_technical_v1_1_0_0_20260608_163510.json"
)
SCHEMA_PATH = REPO_ROOT / "03 Feature Engineering/schemas/feature_snapshot_manifest_schema.json"
GAP_REPORT_REFERENCE = "03 Feature Engineering/docs/gap_report_4h_historical.md"
DECLARED_SERIES_KEYS = {
    ("BTCUSDT", "1d"),
    ("BTCUSDT", "4h"),
    ("ETHUSDT", "1d"),
    ("ETHUSDT", "4h"),
}


def _manifest_payload() -> dict[str, object]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _write_manifest(tmp_path: Path, payload: dict[str, object]) -> Path:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _copy_declared_parquets(tmp_path: Path, payload: dict[str, object]) -> None:
    for series in payload["series"]:
        for parquet_path in series["parquet_paths"]:
            source_path = REPO_ROOT / parquet_path
            target_path = tmp_path / parquet_path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)


def _load_official_snapshot() -> LoadedFeatureSnapshot:
    return FeatureSnapshotLoader(MANIFEST_PATH, schema_path=SCHEMA_PATH).load()


def test_official_manifest_loads_successfully() -> None:
    snapshot = _load_official_snapshot()

    assert snapshot.validation_result.passed is True
    assert snapshot.snapshot_id == "feature_snapshot_technical_v1_1_0_0_20260608_163510"
    assert snapshot.feature_set == "technical_v1"
    assert snapshot.feature_version == "1.0.0"


def test_all_four_declared_series_load() -> None:
    snapshot = _load_official_snapshot()

    assert set(snapshot.series) == DECLARED_SERIES_KEYS


def test_loaded_row_counts_match_manifest() -> None:
    payload = _manifest_payload()
    snapshot = _load_official_snapshot()

    for series_metadata in payload["series"]:
        key = (series_metadata["symbol"], series_metadata["timeframe"])
        assert snapshot.series[key].row_count == series_metadata["row_count"]


def test_loaded_run_id_matches_manifest_series_metadata() -> None:
    payload = _manifest_payload()
    snapshot = _load_official_snapshot()

    for series_metadata in payload["series"]:
        key = (series_metadata["symbol"], series_metadata["timeframe"])
        loaded_series = snapshot.series[key]
        assert loaded_series.run_id == series_metadata["run_id"]
        assert set(loaded_series.frame["run_id"].astype(str).unique()) == {
            series_metadata["run_id"]
        }


def test_loader_rejects_missing_parquet_file(tmp_path: Path) -> None:
    payload = _manifest_payload()
    series = copy.deepcopy(payload["series"])
    run_id = series[0]["run_id"]
    series[0]["parquet_paths"] = [
        f"data/features/technical_v1/1.0.0/BTCUSDT/1d/features_{run_id}_missing.parquet"
    ]
    payload["series"] = series

    loader = FeatureSnapshotLoader(
        _write_manifest(tmp_path, payload),
        schema_path=SCHEMA_PATH,
        repo_root=tmp_path,
    )

    with pytest.raises(FileNotFoundError, match="declared parquet file does not exist"):
        loader.load()


def test_loader_rejects_quarantine_path(tmp_path: Path) -> None:
    payload = _manifest_payload()
    series = copy.deepcopy(payload["series"])
    run_id = series[0]["run_id"]
    series[0]["parquet_paths"] = [
        (
            "data/features/_quarantine/technical_v1/1.0.0/"
            f"BTCUSDT/1d/features_{run_id}.parquet"
        )
    ]
    payload["series"] = series

    loader = FeatureSnapshotLoader(
        _write_manifest(tmp_path, payload),
        schema_path=SCHEMA_PATH,
        repo_root=tmp_path,
    )

    with pytest.raises(ValueError, match="_quarantine"):
        loader.load()


def test_loader_rejects_undeclared_extra_parquet_path(tmp_path: Path) -> None:
    payload = _manifest_payload()
    series = copy.deepcopy(payload["series"])
    series[0]["parquet_paths"] = [
        series[0]["parquet_paths"][0],
        series[0]["parquet_paths"][0],
    ]
    payload["series"] = series
    _copy_declared_parquets(tmp_path, payload)

    loader = FeatureSnapshotLoader(
        _write_manifest(tmp_path, payload),
        schema_path=SCHEMA_PATH,
        repo_root=tmp_path,
    )

    with pytest.raises(ValueError, match="exactly one parquet path"):
        loader.load()


def test_loader_rejects_row_count_mismatch(tmp_path: Path) -> None:
    payload = _manifest_payload()
    _copy_declared_parquets(tmp_path, payload)
    series = copy.deepcopy(payload["series"])
    series[0]["row_count"] = series[0]["row_count"] + 1
    payload["series"] = series

    loader = FeatureSnapshotLoader(
        _write_manifest(tmp_path, payload),
        schema_path=SCHEMA_PATH,
        repo_root=tmp_path,
    )

    with pytest.raises(ValueError, match="loaded row count mismatch"):
        loader.load()


def test_loader_rejects_symbol_timeframe_mismatch(tmp_path: Path) -> None:
    payload = _manifest_payload()
    _copy_declared_parquets(tmp_path, payload)
    first_series = payload["series"][0]
    parquet_path = tmp_path / first_series["parquet_paths"][0]
    frame = pd.read_parquet(parquet_path)
    frame["symbol"] = "XBTUSDT"
    frame.to_parquet(parquet_path, index=False)

    loader = FeatureSnapshotLoader(
        _write_manifest(tmp_path, payload),
        schema_path=SCHEMA_PATH,
        repo_root=tmp_path,
    )

    with pytest.raises(ValueError, match="symbol mismatch"):
        loader.load()


def test_loader_preserves_manifest_path_and_schema_path() -> None:
    snapshot = _load_official_snapshot()

    assert snapshot.manifest_path == MANIFEST_PATH
    assert snapshot.schema_path == SCHEMA_PATH
    assert snapshot.validation_result.manifest_path == MANIFEST_PATH
    assert snapshot.validation_result.schema_path == SCHEMA_PATH


def test_loader_preserves_gap_report_reference() -> None:
    snapshot = _load_official_snapshot()

    assert snapshot.gap_report_reference == GAP_REPORT_REFERENCE


def test_loader_does_not_create_empirical_output_fields() -> None:
    forbidden_names = {
        "metric",
        "metrics",
        "trade",
        "trades",
        "signal",
        "signals",
        "label",
        "labels",
        "pnl",
        "pnL",
    }
    snapshot_field_names = {field.name.lower() for field in fields(LoadedFeatureSnapshot)}
    series_field_names = {field.name.lower() for field in fields(LoadedFeatureSeries)}

    assert snapshot_field_names.isdisjoint(forbidden_names)
    assert series_field_names.isdisjoint(forbidden_names)
