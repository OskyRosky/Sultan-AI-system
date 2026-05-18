from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "research" / "forward_returns.py"
SPEC = importlib.util.spec_from_file_location("research_forward_returns", MODULE_PATH)
forward_returns = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(forward_returns)


def _series_frame(
    *,
    symbol: str = "BTCUSDT",
    timeframe: str = "1h",
    closes: list[float],
    start: str = "2026-01-01 00:00:00",
    freq: str = "1h",
) -> pd.DataFrame:
    timestamps = pd.date_range(start=start, periods=len(closes), freq=freq)
    return pd.DataFrame(
        {
            "symbol": symbol,
            "timeframe": timeframe,
            "timestamp": timestamps,
            "open": closes,
            "high": closes,
            "low": closes,
            "close": closes,
            "volume": 1.0,
        }
    )


def test_forward_returns_align_to_future_closes_and_keep_terminal_nan() -> None:
    frame = _series_frame(closes=[100.0, 110.0, 121.0, 133.1, 146.41])

    result = forward_returns.add_forward_returns(frame, horizons=(1, 3, 5, 10))

    assert result["forward_return_1"].tolist()[:4] == pytest.approx([0.1, 0.1, 0.1, 0.1])
    assert pd.isna(result.loc[result.index[-1], "forward_return_1"])
    assert result.loc[result.index[0], "forward_return_3"] == pytest.approx(133.1 / 100.0 - 1)
    assert result.loc[result.index[1], "forward_return_3"] == pytest.approx(146.41 / 110.0 - 1)
    assert result["forward_return_5"].isna().all()
    assert result["forward_return_10"].isna().all()


def test_no_future_close_column_is_emitted_as_feature_input() -> None:
    frame = _series_frame(closes=[100.0, 101.0, 102.0, 103.0])

    result = forward_returns.add_forward_returns(frame, horizons=(1,))

    assert "future_close" not in result.columns
    assert result.columns.tolist().count("close") == 1
    assert result["close"].tolist() == frame["close"].tolist()


def test_calculation_is_isolated_by_symbol() -> None:
    btc = _series_frame(symbol="BTCUSDT", closes=[100.0, 110.0])
    eth = _series_frame(symbol="ETHUSDT", closes=[1000.0])
    frame = pd.concat([btc, eth], ignore_index=True)

    result = forward_returns.add_forward_returns(frame, horizons=(1,))

    btc_row = result[result["symbol"].eq("BTCUSDT")].iloc[0]
    eth_row = result[result["symbol"].eq("ETHUSDT")].iloc[0]
    assert btc_row["forward_return_1"] == pytest.approx(0.1)
    assert pd.isna(eth_row["forward_return_1"])


def test_calculation_is_isolated_by_timeframe() -> None:
    one_hour = _series_frame(timeframe="1h", closes=[100.0, 110.0], freq="1h")
    four_hour = _series_frame(timeframe="4h", closes=[1000.0], freq="4h")
    frame = pd.concat([one_hour, four_hour], ignore_index=True)

    result = forward_returns.add_forward_returns(frame, horizons=(1,))

    one_hour_row = result[result["timeframe"].eq("1h")].iloc[0]
    four_hour_row = result[result["timeframe"].eq("4h")].iloc[0]
    assert one_hour_row["forward_return_1"] == pytest.approx(0.1)
    assert pd.isna(four_hour_row["forward_return_1"])


def test_duplicate_symbol_timeframe_timestamp_rows_are_rejected() -> None:
    frame = _series_frame(closes=[100.0, 101.0])
    duplicate = frame.iloc[[0]].copy()
    frame = pd.concat([frame, duplicate], ignore_index=True)

    with pytest.raises(ValueError, match="duplicate rows"):
        forward_returns.add_forward_returns(frame, horizons=(1,))


def test_gaps_use_next_available_candle_without_filling_missing_calendar_rows() -> None:
    frame = pd.DataFrame(
        {
            "symbol": ["BTCUSDT", "BTCUSDT", "BTCUSDT"],
            "timeframe": ["1h", "1h", "1h"],
            "timestamp": pd.to_datetime(
                ["2026-01-01 00:00:00", "2026-01-01 01:00:00", "2026-01-01 05:00:00"]
            ),
            "open": [100.0, 110.0, 121.0],
            "high": [100.0, 110.0, 121.0],
            "low": [100.0, 110.0, 121.0],
            "close": [100.0, 110.0, 121.0],
            "volume": [1.0, 1.0, 1.0],
        }
    )

    result = forward_returns.add_forward_returns(frame, horizons=(1,))

    assert len(result) == 3
    assert result.loc[result.index[1], "forward_return_1"] == pytest.approx(121.0 / 110.0 - 1)
    assert pd.isna(result.loc[result.index[2], "forward_return_1"])


def test_input_is_sorted_by_group_and_timestamp_for_deterministic_output() -> None:
    frame = _series_frame(closes=[100.0, 110.0, 121.0])
    shuffled = frame.iloc[[2, 0, 1]].reset_index(drop=True)

    result = forward_returns.add_forward_returns(shuffled, horizons=(1,))

    assert result["timestamp"].tolist() == sorted(frame["timestamp"].tolist())
    assert result["forward_return_1"].tolist()[:2] == pytest.approx([0.1, 0.1])
    assert pd.isna(result.iloc[-1]["forward_return_1"])


def test_forward_return_columns_are_predictable() -> None:
    assert forward_returns.forward_return_columns((1, 3, 3, 10)) == [
        "forward_return_1",
        "forward_return_3",
        "forward_return_10",
    ]
