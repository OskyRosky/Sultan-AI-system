from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import pandas as pd
import pytest

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from feature_storage_contract import STORAGE_FEATURE_COLUMNS, prepare_features_for_storage
from feature_storage_parquet import build_feature_parquet_path, write_features_parquet


def _preview_features_df() -> pd.DataFrame:
    rows = []
    for symbol in ["BTCUSDT", "ETHUSDT"]:
        for timeframe in ["1d", "4h"]:
            row = {
                "exchange": "binance",
                "symbol": symbol,
                "timeframe": timeframe,
                "timestamp": "2026-01-01T00:00:00Z",
                "open": 100.0,
                "high": 101.0,
                "low": 99.0,
                "close": 100.5,
                "volume": 1000.0,
                "feature_set": "technical_v1",
                "feature_version": "1.0.0",
            }
            for feature_index, column in enumerate(STORAGE_FEATURE_COLUMNS):
                row[column] = float(feature_index)
            rows.append(row)
    return pd.DataFrame(rows)


def _storage_df(run_id: str) -> pd.DataFrame:
    return prepare_features_for_storage(
        features_df=_preview_features_df(),
        run_id=run_id,
        integrated_quality_result={
            "ready_for_storage": True,
            "data_quality_score": 0.99,
        },
        validated_at=datetime(2026, 5, 17, 12, 0, tzinfo=timezone.utc),
        created_at=datetime(2026, 5, 17, 12, 1, tzinfo=timezone.utc),
    )


def test_build_feature_parquet_path_matches_expected_structure(tmp_path: Path) -> None:
    run_id = "019e1eb8-a3ba-7de3-ae8e-31874cb9080e"

    result = build_feature_parquet_path(
        base_dir=tmp_path,
        feature_set="technical_v1",
        feature_version="1.0.0",
        symbol="BTCUSDT",
        timeframe="1d",
        run_id=run_id,
    )

    assert result == (
        tmp_path
        / "technical_v1"
        / "1.0.0"
        / "BTCUSDT"
        / "1d"
        / f"features_{run_id}.parquet"
    )


def test_write_features_parquet_creates_file(tmp_path: Path) -> None:
    run_id = str(uuid4())

    paths = write_features_parquet(_storage_df(run_id), base_dir=tmp_path, run_id=run_id)

    assert paths
    assert all(path.exists() for path in paths)


def test_write_features_parquet_writes_one_file_per_symbol_timeframe(
    tmp_path: Path,
) -> None:
    run_id = str(uuid4())

    paths = write_features_parquet(_storage_df(run_id), base_dir=tmp_path, run_id=run_id)

    assert len(paths) == 4


def test_write_features_parquet_excludes_raw_ohlcv_columns(tmp_path: Path) -> None:
    run_id = str(uuid4())
    storage_df = _storage_df(run_id)

    paths = write_features_parquet(storage_df, base_dir=tmp_path, run_id=run_id)
    written = pd.read_parquet(paths[0])

    assert not {"open", "high", "low", "close", "volume"}.intersection(written.columns)


def test_write_features_parquet_includes_run_id(tmp_path: Path) -> None:
    run_id = str(uuid4())

    paths = write_features_parquet(_storage_df(run_id), base_dir=tmp_path, run_id=run_id)
    written = pd.read_parquet(paths[0])

    assert written["run_id"].eq(run_id).all()


def test_write_features_parquet_includes_data_quality_score(tmp_path: Path) -> None:
    run_id = str(uuid4())

    paths = write_features_parquet(_storage_df(run_id), base_dir=tmp_path, run_id=run_id)
    written = pd.read_parquet(paths[0])

    assert written["data_quality_score"].eq(0.99).all()


def test_write_features_parquet_is_idempotent_for_same_run_id(tmp_path: Path) -> None:
    run_id = str(uuid4())
    storage_df = _storage_df(run_id)

    first_paths = write_features_parquet(storage_df, base_dir=tmp_path, run_id=run_id)
    second_paths = write_features_parquet(storage_df, base_dir=tmp_path, run_id=run_id)

    assert second_paths == first_paths
    assert all(path.exists() for path in second_paths)


def test_write_features_parquet_fails_or_skips_empty_dataframe(tmp_path: Path) -> None:
    run_id = str(uuid4())
    storage_df = _storage_df(run_id).iloc[0:0]

    paths = write_features_parquet(storage_df, base_dir=tmp_path, run_id=run_id)

    assert paths == []
    assert list(tmp_path.rglob("*.parquet")) == []


def test_write_features_parquet_fails_with_raw_ohlcv_columns(tmp_path: Path) -> None:
    run_id = str(uuid4())
    storage_df = _storage_df(run_id)
    storage_df["close"] = 100.0

    with pytest.raises(ValueError, match="raw_ohlcv_columns_present"):
        write_features_parquet(storage_df, base_dir=tmp_path, run_id=run_id)
