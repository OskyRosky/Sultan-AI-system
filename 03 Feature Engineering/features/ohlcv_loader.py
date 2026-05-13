"""Read-only OHLCV loader for PostgreSQL curated data."""

from __future__ import annotations

from datetime import datetime

import pandas as pd

from config import FeatureSettings, build_postgres_dsn, load_feature_settings


OHLCV_SELECT_COLUMNS = [
    "exchange",
    "symbol",
    "timeframe",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
]


def load_ohlcv_read_only(
    symbol: str,
    timeframe: str,
    start_timestamp: datetime | str | None = None,
    end_timestamp: datetime | str | None = None,
    limit: int | None = None,
    settings: FeatureSettings | None = None,
) -> pd.DataFrame:
    """Load OHLCV from PostgreSQL using SELECT only."""

    import psycopg2

    selected_settings = settings or load_feature_settings()
    table_name = _validate_table_name(selected_settings.ohlcv_table)
    query_parts = [
        f"""
        SELECT
            exchange,
            symbol,
            timeframe,
            timestamp,
            open,
            high,
            low,
            close,
            volume
        FROM {table_name}
        WHERE symbol = %s
          AND timeframe = %s
        """
    ]
    params: list[object] = [symbol, timeframe]

    if start_timestamp is not None:
        query_parts.append("AND timestamp >= %s")
        params.append(start_timestamp)
    if end_timestamp is not None:
        query_parts.append("AND timestamp <= %s")
        params.append(end_timestamp)

    query_parts.append("ORDER BY symbol, timeframe, timestamp")
    if limit is not None:
        safe_limit = int(limit)
        if safe_limit <= 0:
            raise ValueError("limit must be positive when provided")
        query_parts.append("LIMIT %s")
        params.append(safe_limit)

    query = "\n".join(query_parts)
    with psycopg2.connect(
        build_postgres_dsn(selected_settings.postgres), connect_timeout=5
    ) as connection:
        connection.set_session(readonly=True, autocommit=True)
        return pd.read_sql_query(query, connection, params=params)


def load_ohlcv_batch_read_only(
    symbols: list[str] | tuple[str, ...],
    timeframes: list[str] | tuple[str, ...],
    limit: int | None = None,
    settings: FeatureSettings | None = None,
) -> pd.DataFrame:
    """Load multiple symbol/timeframe slices and concatenate them."""

    frames = [
        load_ohlcv_read_only(
            symbol=symbol,
            timeframe=timeframe,
            limit=limit,
            settings=settings,
        )
        for symbol in symbols
        for timeframe in timeframes
    ]
    if not frames:
        return pd.DataFrame(columns=OHLCV_SELECT_COLUMNS)
    return pd.concat(frames, ignore_index=True)


def _validate_table_name(table_name: str) -> str:
    parts = table_name.split(".")
    if len(parts) != 2 or not all(part.isidentifier() for part in parts):
        raise ValueError(f"Invalid table name: {table_name}")
    return table_name
