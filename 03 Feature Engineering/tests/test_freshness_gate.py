from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from freshness_gate import evaluate_freshness_timestamp


def test_freshness_passes_when_lag_within_threshold() -> None:
    current_time = pd.Timestamp("2026-05-17T12:00:00Z")
    latest_timestamp = current_time - pd.Timedelta(hours=6)

    result = evaluate_freshness_timestamp(
        symbol="BTCUSDT",
        timeframe="1d",
        latest_timestamp=latest_timestamp,
        current_time=current_time,
    )

    assert result.passed is True
    assert result.status == "passed"


def test_freshness_fails_when_lag_exceeds_threshold() -> None:
    current_time = pd.Timestamp("2026-05-17T12:00:00Z")
    latest_timestamp = current_time - pd.Timedelta(days=3)

    result = evaluate_freshness_timestamp(
        symbol="BTCUSDT",
        timeframe="1d",
        latest_timestamp=latest_timestamp,
        current_time=current_time,
    )

    assert result.passed is False
    assert result.status == "failed"
    assert result.message == "Freshness lag exceeds threshold."


def test_freshness_fails_when_latest_timestamp_is_none() -> None:
    current_time = pd.Timestamp("2026-05-17T12:00:00Z")

    result = evaluate_freshness_timestamp(
        symbol="BTCUSDT",
        timeframe="1d",
        latest_timestamp=None,
        current_time=current_time,
    )

    assert result.passed is False
    assert result.status == "failed"
    assert result.latest_timestamp is None
    assert result.message == "No OHLCV rows found for symbol/timeframe."


def test_freshness_fails_or_reports_unsupported_timeframe() -> None:
    current_time = pd.Timestamp("2026-05-17T12:00:00Z")

    result = evaluate_freshness_timestamp(
        symbol="BTCUSDT",
        timeframe="15m",
        latest_timestamp=current_time,
        current_time=current_time,
    )

    assert result.passed is False
    assert result.status == "failed"
    assert result.max_allowed_lag == "unsupported_timeframe"
    assert result.message == "Unsupported timeframe for freshness gate: 15m"
