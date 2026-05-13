"""Freshness gate for read-only OHLCV checks."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any

import pandas as pd

from config import FeatureSettings, build_postgres_dsn, load_feature_settings
from ohlcv_loader import _validate_table_name


MAX_ALLOWED_LAG = {
    "1d": timedelta(days=2),
    "4h": timedelta(hours=12),
}


@dataclass(frozen=True)
class FreshnessGateResult:
    status: str
    symbol: str
    timeframe: str
    latest_timestamp: str | None
    current_time: str
    max_allowed_lag: str
    observed_lag: str | None
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "latest_timestamp": self.latest_timestamp,
            "current_time": self.current_time,
            "max_allowed_lag": self.max_allowed_lag,
            "observed_lag": self.observed_lag,
            "passed": self.passed,
            "message": self.message,
        }


def check_ohlcv_freshness(
    symbol: str,
    timeframe: str,
    settings: FeatureSettings | None = None,
) -> FreshnessGateResult:
    """Read latest OHLCV timestamp and evaluate freshness without side effects."""

    import psycopg2

    selected_settings = settings or load_feature_settings()
    table_name = _validate_table_name(selected_settings.ohlcv_table)
    max_allowed_lag = MAX_ALLOWED_LAG.get(timeframe)
    current_time = pd.Timestamp.now(tz="UTC")

    if max_allowed_lag is None:
        return FreshnessGateResult(
            status="failed",
            symbol=symbol,
            timeframe=timeframe,
            latest_timestamp=None,
            current_time=current_time.isoformat(),
            max_allowed_lag="unsupported_timeframe",
            observed_lag=None,
            passed=False,
            message=f"Unsupported timeframe for freshness gate: {timeframe}",
        )

    query = f"""
        SELECT MAX(timestamp) AS latest_timestamp
        FROM {table_name}
        WHERE symbol = %s
          AND timeframe = %s
    """
    with psycopg2.connect(
        build_postgres_dsn(selected_settings.postgres), connect_timeout=5
    ) as connection:
        connection.set_session(readonly=True, autocommit=True)
        with connection.cursor() as cursor:
            cursor.execute(query, (symbol, timeframe))
            latest_timestamp = cursor.fetchone()[0]

    return evaluate_freshness_timestamp(
        symbol=symbol,
        timeframe=timeframe,
        latest_timestamp=latest_timestamp,
        current_time=current_time,
    )


def evaluate_freshness_timestamp(
    symbol: str,
    timeframe: str,
    latest_timestamp: object,
    current_time: pd.Timestamp | None = None,
) -> FreshnessGateResult:
    """Evaluate freshness from an already available timestamp."""

    now_utc = current_time if current_time is not None else pd.Timestamp.now(tz="UTC")
    max_allowed_lag = MAX_ALLOWED_LAG.get(timeframe)
    if max_allowed_lag is None:
        return FreshnessGateResult(
            status="failed",
            symbol=symbol,
            timeframe=timeframe,
            latest_timestamp=None,
            current_time=now_utc.isoformat(),
            max_allowed_lag="unsupported_timeframe",
            observed_lag=None,
            passed=False,
            message=f"Unsupported timeframe for freshness gate: {timeframe}",
        )

    if latest_timestamp is None:
        return FreshnessGateResult(
            status="failed",
            symbol=symbol,
            timeframe=timeframe,
            latest_timestamp=None,
            current_time=now_utc.isoformat(),
            max_allowed_lag=str(max_allowed_lag),
            observed_lag=None,
            passed=False,
            message="No OHLCV rows found for symbol/timeframe.",
        )

    latest = pd.Timestamp(latest_timestamp)
    if latest.tzinfo is None:
        latest = latest.tz_localize("UTC")
    else:
        latest = latest.tz_convert("UTC")

    observed_lag = now_utc - latest
    passed = observed_lag <= max_allowed_lag
    return FreshnessGateResult(
        status="passed" if passed else "failed",
        symbol=symbol,
        timeframe=timeframe,
        latest_timestamp=latest.isoformat(),
        current_time=now_utc.isoformat(),
        max_allowed_lag=str(max_allowed_lag),
        observed_lag=str(observed_lag),
        passed=passed,
        message="Freshness gate passed." if passed else "Freshness lag exceeds threshold.",
    )
