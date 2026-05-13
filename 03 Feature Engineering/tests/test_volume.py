from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from volume import calculate_volume_features


def _ohlcv_dataframe() -> pd.DataFrame:
    rows = []
    for symbol, timeframe, base_volume in [
        ("BTCUSDT", "1d", 1000.0),
        ("ETHUSDT", "4h", 2000.0),
    ]:
        for index in range(60):
            close = 100.0 + index
            rows.append(
                {
                    "exchange": "binance",
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "timestamp": pd.Timestamp("2026-01-01T00:00:00Z")
                    + pd.Timedelta(hours=index if timeframe == "4h" else index * 24),
                    "open": close - 0.5,
                    "high": close + 1.0,
                    "low": close - 1.0,
                    "close": close,
                    "volume": base_volume + index * 10.0,
                }
            )
    return pd.DataFrame(rows)


def test_calculate_volume_adds_expected_columns() -> None:
    result = calculate_volume_features(_ohlcv_dataframe())

    assert "volume_change" in result.columns
    assert "volume_sma_20" in result.columns
    assert "volume_ratio_20" in result.columns


def test_volume_change_is_correct() -> None:
    result = calculate_volume_features(_ohlcv_dataframe())
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert np.isclose(btc.loc[1, "volume_change"], 1010.0 / 1000.0 - 1.0)


def test_volume_sma_20_is_correct() -> None:
    result = calculate_volume_features(_ohlcv_dataframe())
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert np.isclose(btc.loc[19, "volume_sma_20"], np.mean(np.arange(1000.0, 1200.0, 10.0)))


def test_volume_ratio_20_is_correct() -> None:
    result = calculate_volume_features(_ohlcv_dataframe())
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    expected_sma = np.mean(np.arange(1000.0, 1200.0, 10.0))
    assert np.isclose(btc.loc[19, "volume_ratio_20"], 1190.0 / expected_sma)


def test_volume_is_grouped_by_symbol_and_timeframe() -> None:
    result = calculate_volume_features(_ohlcv_dataframe())
    eth = result[result["symbol"] == "ETHUSDT"].reset_index(drop=True)

    assert pd.isna(eth.loc[0, "volume_change"])
    assert np.isclose(eth.loc[1, "volume_change"], 2010.0 / 2000.0 - 1.0)


def test_original_dataframe_is_not_modified() -> None:
    df = _ohlcv_dataframe()
    original_columns = list(df.columns)

    calculate_volume_features(df)

    assert list(df.columns) == original_columns


def test_no_infinite_values_for_valid_positive_volume() -> None:
    result = calculate_volume_features(_ohlcv_dataframe())
    values = result[["volume_change", "volume_sma_20", "volume_ratio_20"]].to_numpy()

    assert not np.isinf(values[~pd.isna(values)]).any()


def test_volume_change_first_row_is_nan() -> None:
    result = calculate_volume_features(_ohlcv_dataframe())
    first_rows = result.groupby(["exchange", "symbol", "timeframe"]).head(1)

    assert first_rows["volume_change"].isna().all()


def test_volume_sma_20_warmup_is_nan() -> None:
    result = calculate_volume_features(_ohlcv_dataframe())
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert btc.loc[:18, "volume_sma_20"].isna().all()
    assert btc.loc[:18, "volume_ratio_20"].isna().all()


def test_auxiliary_columns_not_in_output() -> None:
    result = calculate_volume_features(_ohlcv_dataframe())

    assert "previous_volume" not in result.columns
