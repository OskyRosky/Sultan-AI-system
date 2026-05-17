from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import numpy as np
import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

import feature_storage_db
from feature_storage_contract import STORAGE_FEATURE_COLUMNS, prepare_features_for_storage
from feature_storage_db import (
    build_insert_feature_run_payload,
    build_ohlcv_features_upsert_sql,
    build_quality_check_records,
    dataframe_records_for_postgres,
    store_features_postgres,
)


class FakeCursor:
    def __init__(self, connection: FakeConnection) -> None:
        self.connection = connection

    def __enter__(self) -> FakeCursor:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def execute(self, sql: str, values: list[object]) -> None:
        self.connection.executed.append((sql, values))


class FakeConnection:
    def __init__(self) -> None:
        self.executed: list[tuple[str, list[object]]] = []

    def cursor(self) -> FakeCursor:
        return FakeCursor(self)


def _preview_features_df() -> pd.DataFrame:
    rows = []
    for index in range(2):
        row = {
            "exchange": "binance",
            "symbol": "BTCUSDT",
            "timeframe": "1d",
            "timestamp": pd.Timestamp("2026-01-01T00:00:00Z")
            + pd.Timedelta(days=index),
            "open": 100.0,
            "high": 101.0,
            "low": 99.0,
            "close": 100.5,
            "volume": 1000.0,
            "feature_set": "technical_v1",
            "feature_version": "1.0.0",
        }
        for feature_index, column in enumerate(STORAGE_FEATURE_COLUMNS):
            row[column] = float(index + feature_index)
        rows.append(row)
    return pd.DataFrame(rows)


def _storage_df(run_id: str) -> pd.DataFrame:
    return prepare_features_for_storage(
        features_df=_preview_features_df(),
        run_id=run_id,
        integrated_quality_result={
            "ready_for_storage": True,
            "data_quality_score": 1.0,
        },
        validated_at=datetime(2026, 5, 17, 12, 0, tzinfo=timezone.utc),
        created_at=datetime(2026, 5, 17, 12, 1, tzinfo=timezone.utc),
    )


def _integrated_result(ready_for_storage: bool = True) -> dict[str, object]:
    return {
        "status": "passed" if ready_for_storage else "failed",
        "ready_for_storage": ready_for_storage,
        "data_quality_score": 1.0 if ready_for_storage else 0.5,
        "rows_checked": 2,
        "blocking_errors": [] if ready_for_storage else ["missing_expected_columns=['macd']"],
        "warnings": [],
        "missing_columns": [] if ready_for_storage else ["macd"],
        "unexpected_columns": [],
        "forbidden_columns_found": [],
        "duplicate_count": 0,
        "infinite_count": 0,
        "null_counts_by_family": {"momentum": {"rsi_14": 1}},
    }


def test_build_insert_feature_run_payload_contains_required_fields() -> None:
    run_id = uuid4()

    payload = build_insert_feature_run_payload(
        run_id=run_id,
        flow_name="generate_features_flow",
        symbols=["BTCUSDT"],
        timeframes=["1d"],
        rows_loaded=2,
        rows_generated=2,
        rows_validated=2,
    )

    assert payload["run_id"] == str(run_id)
    assert payload["flow_name"] == "generate_features_flow"
    assert payload["status"] == "running"
    assert payload["feature_set"] == "technical_v1"
    assert payload["feature_version"] == "1.0.0"
    assert payload["rows_loaded"] == 2


def test_build_quality_check_records_includes_integrated() -> None:
    records = build_quality_check_records(
        run_id="019e1eb8-a3ba-7de3-ae8e-31874cb9080e",
        integrated_quality_result=_integrated_result(),
    )

    assert len(records) == 1
    assert records[0]["check_name"] == "integrated"
    assert records[0]["check_status"] == "passed"
    assert records[0]["nulls_found"] == 1


def test_build_quality_check_records_includes_family_checks_when_provided() -> None:
    records = build_quality_check_records(
        run_id="019e1eb8-a3ba-7de3-ae8e-31874cb9080e",
        integrated_quality_result=_integrated_result(),
        family_quality_results={
            "momentum": {
                "status": "failed",
                "passed": False,
                "rows_checked": 2,
                "errors": ["macd_unexpected_nan=1"],
                "warnings": [],
            }
        },
    )

    assert [record["check_name"] for record in records] == ["integrated", "momentum"]
    assert records[1]["severity"] == "blocking"


def test_build_ohlcv_features_upsert_sql_uses_expected_conflict_key() -> None:
    sql = build_ohlcv_features_upsert_sql()

    assert (
        "ON CONFLICT (exchange, symbol, timeframe, timestamp, feature_set, feature_version)"
        in " ".join(sql.split())
    )


def test_build_ohlcv_features_upsert_sql_does_not_update_created_at() -> None:
    sql = build_ohlcv_features_upsert_sql()
    update_clause = sql.split("DO UPDATE", maxsplit=1)[1]

    assert "created_at = EXCLUDED.created_at" not in update_clause


def test_upsert_sql_excludes_raw_ohlcv_columns() -> None:
    sql = build_ohlcv_features_upsert_sql()
    insert_columns = (
        sql.split("INSERT INTO ohlcv_features (", maxsplit=1)[1]
        .split(")", maxsplit=1)[0]
        .replace("\n", "")
        .split(", ")
    )

    assert not {"open", "high", "low", "close", "volume"}.intersection(insert_columns)


def test_dataframe_records_convert_nan_to_none() -> None:
    records = dataframe_records_for_postgres(pd.DataFrame({"value": [np.nan]}))

    assert records == [{"value": None}]


def test_dataframe_records_convert_timestamps() -> None:
    records = dataframe_records_for_postgres(
        pd.DataFrame({"timestamp": [pd.Timestamp("2026-05-17T12:00:00Z")]})
    )

    assert records[0]["timestamp"].tzinfo is not None
    assert records[0]["timestamp"].isoformat() == "2026-05-17T12:00:00+00:00"


def test_store_features_postgres_skips_upsert_when_ready_for_storage_false(
    monkeypatch,
) -> None:
    calls = {"upsert": 0}

    def fake_upsert(_conn, _storage_df):
        calls["upsert"] += 1
        return 2

    monkeypatch.setattr(feature_storage_db, "upsert_ohlcv_features", fake_upsert)

    result = store_features_postgres(
        conn=FakeConnection(),
        storage_df=_storage_df("019e1eb8-a3ba-7de3-ae8e-31874cb9080e"),
        run_payload=build_insert_feature_run_payload(
            run_id="019e1eb8-a3ba-7de3-ae8e-31874cb9080e",
            flow_name="generate_features_flow",
        ),
        integrated_quality_result=_integrated_result(ready_for_storage=False),
    )

    assert calls["upsert"] == 0
    assert result["features_upserted"] is False


def test_store_features_postgres_calls_upsert_when_ready_for_storage_true(
    monkeypatch,
) -> None:
    calls = {"upsert": 0}

    def fake_upsert(_conn, _storage_df):
        calls["upsert"] += 1
        return 2

    monkeypatch.setattr(feature_storage_db, "upsert_ohlcv_features", fake_upsert)

    result = store_features_postgres(
        conn=FakeConnection(),
        storage_df=_storage_df("019e1eb8-a3ba-7de3-ae8e-31874cb9080e"),
        run_payload=build_insert_feature_run_payload(
            run_id="019e1eb8-a3ba-7de3-ae8e-31874cb9080e",
            flow_name="generate_features_flow",
        ),
        integrated_quality_result=_integrated_result(ready_for_storage=True),
    )

    assert calls["upsert"] == 1
    assert result["features_upserted"] is True
    assert result["rows_inserted"] == 2


def test_store_features_postgres_updates_run_failed_when_gate_blocks() -> None:
    conn = FakeConnection()

    store_features_postgres(
        conn=conn,
        storage_df=_storage_df("019e1eb8-a3ba-7de3-ae8e-31874cb9080e"),
        run_payload=build_insert_feature_run_payload(
            run_id="019e1eb8-a3ba-7de3-ae8e-31874cb9080e",
            flow_name="generate_features_flow",
        ),
        integrated_quality_result=_integrated_result(ready_for_storage=False),
    )

    update_calls = [item for item in conn.executed if "UPDATE feature_runs" in item[0]]
    assert update_calls
    assert update_calls[-1][1][1] == "failed"
    assert update_calls[-1][1][2] == 0


def test_store_features_postgres_updates_run_passed_when_upsert_succeeds() -> None:
    conn = FakeConnection()

    store_features_postgres(
        conn=conn,
        storage_df=_storage_df("019e1eb8-a3ba-7de3-ae8e-31874cb9080e"),
        run_payload=build_insert_feature_run_payload(
            run_id="019e1eb8-a3ba-7de3-ae8e-31874cb9080e",
            flow_name="generate_features_flow",
        ),
        integrated_quality_result=_integrated_result(ready_for_storage=True),
        parquet_paths=[Path("data/features/technical_v1/1.0.0/BTCUSDT/1d/file.parquet")],
    )

    update_calls = [item for item in conn.executed if "UPDATE feature_runs" in item[0]]
    assert update_calls
    assert update_calls[-1][1][1] == "passed"
    assert update_calls[-1][1][2] == 2
    metadata = json.loads(update_calls[-1][1][4])
    assert metadata["ready_for_storage"] is True
    assert metadata["parquet_paths"] == [
        "data/features/technical_v1/1.0.0/BTCUSDT/1d/file.parquet"
    ]
