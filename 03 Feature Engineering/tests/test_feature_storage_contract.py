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

from feature_storage_contract import (
    RAW_OHLCV_COLUMNS_EXCLUDED_FROM_FEATURE_STORAGE,
    STORAGE_FEATURE_COLUMNS,
    get_raw_ohlcv_columns_excluded_from_storage,
    get_storage_columns,
    prepare_features_for_storage,
    validate_storage_contract_columns,
)


def _preview_features_df() -> pd.DataFrame:
    rows = []
    for symbol in ["BTCUSDT", "ETHUSDT"]:
        for index in range(2):
            row = {
                "exchange": "binance",
                "symbol": symbol,
                "timeframe": "1d",
                "timestamp": pd.Timestamp("2026-01-01T00:00:00Z")
                + pd.Timedelta(days=index),
                "open": 100.0 + index,
                "high": 101.0 + index,
                "low": 99.0 + index,
                "close": 100.5 + index,
                "volume": 1000.0 + index,
                "feature_set": "technical_v1",
                "feature_version": "1.0.0",
            }
            for feature_index, column in enumerate(STORAGE_FEATURE_COLUMNS):
                row[column] = float(index + feature_index)
            rows.append(row)
    return pd.DataFrame(rows)


def _quality_result(ready_for_storage: bool = True) -> dict[str, object]:
    return {
        "ready_for_storage": ready_for_storage,
        "data_quality_score": 1.0,
    }


def _storage_df() -> pd.DataFrame:
    return prepare_features_for_storage(
        features_df=_preview_features_df(),
        run_id="019e1eb8-a3ba-7de3-ae8e-31874cb9080e",
        integrated_quality_result=_quality_result(),
        validated_at=datetime(2026, 5, 17, 12, 0, tzinfo=timezone.utc),
        created_at=datetime(2026, 5, 17, 12, 1, tzinfo=timezone.utc),
    )


def test_get_storage_columns_includes_27_features() -> None:
    assert len(STORAGE_FEATURE_COLUMNS) == 27
    assert set(STORAGE_FEATURE_COLUMNS).issubset(set(get_storage_columns()))


def test_storage_columns_exclude_raw_ohlcv_columns() -> None:
    storage_columns = set(get_storage_columns())

    assert not storage_columns.intersection(RAW_OHLCV_COLUMNS_EXCLUDED_FROM_FEATURE_STORAGE)
    assert get_raw_ohlcv_columns_excluded_from_storage() == [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]


def test_prepare_features_for_storage_adds_run_id() -> None:
    run_id = uuid4()

    result = prepare_features_for_storage(
        _preview_features_df(),
        run_id=run_id,
        integrated_quality_result=_quality_result(),
    )

    assert result["run_id"].eq(str(run_id)).all()


def test_prepare_features_for_storage_adds_validated_at() -> None:
    validated_at = datetime(2026, 5, 17, 12, 0, tzinfo=timezone.utc)

    result = prepare_features_for_storage(
        _preview_features_df(),
        run_id=uuid4(),
        integrated_quality_result=_quality_result(),
        validated_at=validated_at,
    )

    assert result["validated_at"].eq(pd.Timestamp(validated_at)).all()


def test_prepare_features_for_storage_adds_data_quality_score() -> None:
    result = prepare_features_for_storage(
        _preview_features_df(),
        run_id=uuid4(),
        integrated_quality_result={"ready_for_storage": True, "data_quality_score": 0.97},
    )

    assert result["data_quality_score"].eq(0.97).all()


def test_prepare_features_for_storage_excludes_raw_ohlcv_columns() -> None:
    result = prepare_features_for_storage(
        _preview_features_df(),
        run_id=uuid4(),
        integrated_quality_result=_quality_result(),
    )

    assert not set(result.columns).intersection(RAW_OHLCV_COLUMNS_EXCLUDED_FROM_FEATURE_STORAGE)


def test_prepare_features_for_storage_does_not_modify_input_in_place() -> None:
    preview = _preview_features_df()
    original_columns = list(preview.columns)

    prepare_features_for_storage(
        preview,
        run_id=uuid4(),
        integrated_quality_result=_quality_result(),
    )

    assert list(preview.columns) == original_columns
    assert "run_id" not in preview.columns


def test_prepare_features_for_storage_fails_when_ready_for_storage_false() -> None:
    with pytest.raises(ValueError, match="integrated_quality_result_not_ready"):
        prepare_features_for_storage(
            _preview_features_df(),
            run_id=uuid4(),
            integrated_quality_result=_quality_result(ready_for_storage=False),
        )


def test_prepare_features_for_storage_fails_when_required_feature_missing() -> None:
    preview = _preview_features_df().drop(columns=["macd"])

    with pytest.raises(ValueError, match="missing_required_storage_source_columns"):
        prepare_features_for_storage(
            preview,
            run_id=uuid4(),
            integrated_quality_result=_quality_result(),
        )


def test_validate_storage_contract_passes_for_clean_storage_df() -> None:
    result = validate_storage_contract_columns(_storage_df())

    assert result["passed"] is True
    assert result["errors"] == []


def test_validate_storage_contract_fails_with_raw_ohlcv_columns() -> None:
    storage_df = _storage_df()
    storage_df["close"] = 100.0

    result = validate_storage_contract_columns(storage_df)

    assert result["passed"] is False
    assert "raw_ohlcv_columns_present=['close']" in result["errors"]
