from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from ohlcv_validation import detect_temporal_gaps, validate_ohlcv_dataframe


def _row(timestamp: str, timeframe: str = "1d") -> dict[str, object]:
    return {
        "exchange": "binance",
        "symbol": "BTCUSDT",
        "timeframe": timeframe,
        "timestamp": pd.Timestamp(timestamp),
        "open": 100.0,
        "high": 101.0,
        "low": 99.0,
        "close": 100.5,
        "volume": 10.0,
    }


def test_detect_temporal_gaps_reports_1d_gap_without_blocking_validation() -> None:
    df = pd.DataFrame(
        [
            _row("2026-01-01T00:00:00Z"),
            _row("2026-01-02T00:00:00Z"),
            _row("2026-01-04T00:00:00Z"),
        ]
    )

    result = validate_ohlcv_dataframe(df)

    assert result.passed
    assert any("temporal_gaps_detected=binance/BTCUSDT/1d" in item for item in result.warnings)


def test_detect_temporal_gaps_reports_4h_gap() -> None:
    df = pd.DataFrame(
        [
            _row("2026-01-01T00:00:00Z", "4h"),
            _row("2026-01-01T04:00:00Z", "4h"),
            _row("2026-01-01T12:00:00Z", "4h"),
        ]
    )

    warnings = detect_temporal_gaps(df)

    assert any("temporal_gaps_detected=binance/BTCUSDT/4h" in item for item in warnings)


def test_detect_temporal_gaps_returns_empty_for_contiguous_series() -> None:
    df = pd.DataFrame(
        [
            _row("2026-01-01T00:00:00Z"),
            _row("2026-01-02T00:00:00Z"),
            _row("2026-01-03T00:00:00Z"),
        ]
    )

    assert detect_temporal_gaps(df) == []
