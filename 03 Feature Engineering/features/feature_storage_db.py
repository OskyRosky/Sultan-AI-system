"""PostgreSQL write-path helpers for feature storage.

This module builds and executes SQL against a provided connection. It does not
open database connections or manage DDL.
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any
from uuid import UUID

import numpy as np
import pandas as pd

from config import FEATURE_SET, FEATURE_VERSION
from feature_storage_contract import (
    STORAGE_COLUMNS,
    STORAGE_FEATURE_COLUMNS,
    validate_storage_contract_columns,
)


FEATURE_RUN_COLUMNS = [
    "run_id",
    "flow_name",
    "status",
    "started_at",
    "finished_at",
    "feature_set",
    "feature_version",
    "symbols",
    "timeframes",
    "rows_loaded",
    "rows_generated",
    "rows_validated",
    "rows_inserted",
    "error_message",
    "metadata",
]

QUALITY_CHECK_COLUMNS = [
    "run_id",
    "check_name",
    "check_status",
    "severity",
    "rows_checked",
    "rows_failed",
    "nulls_found",
    "infinities_found",
    "duplicates_found",
    "lookahead_violations",
    "data_quality_score",
    "error_message",
    "metadata",
]

OHLCV_FEATURES_CONFLICT_COLUMNS = [
    "exchange",
    "symbol",
    "timeframe",
    "timestamp",
    "feature_set",
    "feature_version",
]

POSTGRES_BOOLEAN_COLUMNS = {
    "price_above_sma20",
    "ema20_above_ema50",
}


def build_insert_feature_run_payload(
    *,
    run_id: str | UUID,
    flow_name: str,
    status: str = "running",
    started_at: datetime | None = None,
    finished_at: datetime | None = None,
    feature_set: str = FEATURE_SET,
    feature_version: str = FEATURE_VERSION,
    symbols: list[str] | tuple[str, ...] | None = None,
    timeframes: list[str] | tuple[str, ...] | None = None,
    rows_loaded: int = 0,
    rows_generated: int = 0,
    rows_validated: int = 0,
    rows_inserted: int = 0,
    error_message: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "run_id": str(run_id),
        "flow_name": flow_name,
        "status": status,
        "started_at": _as_utc_timestamp(started_at or datetime.now(timezone.utc)),
        "finished_at": _as_utc_timestamp(finished_at) if finished_at else None,
        "feature_set": feature_set,
        "feature_version": feature_version,
        "symbols": list(symbols or []),
        "timeframes": list(timeframes or []),
        "rows_loaded": int(rows_loaded),
        "rows_generated": int(rows_generated),
        "rows_validated": int(rows_validated),
        "rows_inserted": int(rows_inserted),
        "error_message": error_message,
        "metadata": dict(metadata or {}),
    }


def insert_feature_run(conn: Any, payload: dict[str, Any]) -> str:
    placeholders = ", ".join(["%s"] * len(FEATURE_RUN_COLUMNS))
    columns_sql = ", ".join(FEATURE_RUN_COLUMNS)
    sql = f"""
        INSERT INTO feature_runs ({columns_sql})
        VALUES ({placeholders})
    """
    values = [normalize_value_for_postgres(payload.get(column)) for column in FEATURE_RUN_COLUMNS]
    with conn.cursor() as cursor:
        cursor.execute(sql, values)
    return str(payload["run_id"])


def update_feature_run_finished(
    conn: Any,
    run_id: str | UUID,
    status: str,
    rows_inserted: int,
    error_message: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> None:
    sql = """
        UPDATE feature_runs
        SET finished_at = %s,
            status = %s,
            rows_inserted = %s,
            error_message = %s,
            metadata = %s
        WHERE run_id = %s
    """
    values = [
        _as_utc_timestamp(datetime.now(timezone.utc)),
        status,
        int(rows_inserted),
        error_message,
        normalize_value_for_postgres(metadata or {}),
        str(run_id),
    ]
    with conn.cursor() as cursor:
        cursor.execute(sql, values)


def build_quality_check_records(
    run_id: str | UUID,
    integrated_quality_result: dict[str, Any],
    family_quality_results: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    records = [_quality_record_from_integrated(run_id, integrated_quality_result)]
    for family_name, result in (family_quality_results or {}).items():
        records.append(_quality_record_from_family(run_id, family_name, result))
    return records


def insert_feature_quality_checks(conn: Any, records: list[dict[str, Any]]) -> int:
    if not records:
        return 0

    placeholders = ", ".join(["%s"] * len(QUALITY_CHECK_COLUMNS))
    columns_sql = ", ".join(QUALITY_CHECK_COLUMNS)
    sql = f"""
        INSERT INTO feature_quality_checks ({columns_sql})
        VALUES ({placeholders})
    """
    with conn.cursor() as cursor:
        for record in records:
            values = [
                normalize_value_for_postgres(record.get(column))
                for column in QUALITY_CHECK_COLUMNS
            ]
            cursor.execute(sql, values)
    return len(records)


def build_ohlcv_features_upsert_sql() -> str:
    columns_sql = ", ".join(STORAGE_COLUMNS)
    placeholders = ", ".join(["%s"] * len(STORAGE_COLUMNS))
    conflict_sql = ", ".join(OHLCV_FEATURES_CONFLICT_COLUMNS)
    update_columns = [
        "run_id",
        "validated_at",
        "data_quality_score",
        *STORAGE_FEATURE_COLUMNS,
    ]
    update_sql = ",\n            ".join(
        f"{column} = EXCLUDED.{column}" for column in update_columns
    )
    return f"""
        INSERT INTO ohlcv_features ({columns_sql})
        VALUES ({placeholders})
        ON CONFLICT ({conflict_sql}) DO UPDATE
        SET {update_sql}
    """


def upsert_ohlcv_features(conn: Any, storage_df: pd.DataFrame) -> int:
    contract_result = validate_storage_contract_columns(storage_df)
    if not contract_result["passed"]:
        raise ValueError(f"storage_contract_failed={contract_result['errors']}")
    if storage_df.empty:
        return 0

    sql = build_ohlcv_features_upsert_sql()
    records = dataframe_records_for_postgres(storage_df.loc[:, STORAGE_COLUMNS])
    with conn.cursor() as cursor:
        for record in records:
            cursor.execute(sql, [record[column] for column in STORAGE_COLUMNS])
    return len(records)


def store_features_postgres(
    *,
    conn: Any,
    storage_df: pd.DataFrame,
    run_payload: dict[str, Any],
    integrated_quality_result: dict[str, Any],
    family_quality_results: dict[str, dict[str, Any]] | None = None,
    parquet_paths: list[str | Path] | None = None,
) -> dict[str, Any]:
    run_id = insert_feature_run(conn, run_payload)
    quality_records = build_quality_check_records(
        run_id=run_id,
        integrated_quality_result=integrated_quality_result,
        family_quality_results=family_quality_results,
    )
    metadata = _run_completion_metadata(
        integrated_quality_result=integrated_quality_result,
        parquet_paths=parquet_paths,
    )

    if not integrated_quality_result.get("ready_for_storage"):
        quality_checks_inserted = insert_feature_quality_checks(conn, quality_records)
        update_feature_run_finished(
            conn=conn,
            run_id=run_id,
            status="failed",
            rows_inserted=0,
            error_message="ready_for_storage_false",
            metadata=metadata,
        )
        return {
            "run_id": run_id,
            "status": "failed",
            "rows_inserted": 0,
            "quality_checks_inserted": quality_checks_inserted,
            "features_upserted": False,
        }

    rows_inserted = upsert_ohlcv_features(conn, storage_df)
    quality_checks_inserted = insert_feature_quality_checks(conn, quality_records)
    update_feature_run_finished(
        conn=conn,
        run_id=run_id,
        status="passed",
        rows_inserted=rows_inserted,
        error_message=None,
        metadata=metadata,
    )
    return {
        "run_id": run_id,
        "status": "passed",
        "rows_inserted": rows_inserted,
        "quality_checks_inserted": quality_checks_inserted,
        "features_upserted": True,
    }


def dataframe_records_for_postgres(df: pd.DataFrame) -> list[dict[str, Any]]:
    return [
        {
            column: (
                normalize_boolean_for_postgres(value, column)
                if column in POSTGRES_BOOLEAN_COLUMNS
                else normalize_value_for_postgres(value)
            )
            for column, value in row.items()
        }
        for row in df.to_dict(orient="records")
    ]


def normalize_boolean_for_postgres(value: Any, column: str) -> bool | None:
    if value is None:
        return None
    if value is pd.NA or value is pd.NaT:
        return None
    if isinstance(value, float):
        if math.isnan(value):
            return None
        if value == 1.0:
            return True
        if value == 0.0:
            return False
        raise ValueError(f"invalid_boolean_value_for_{column}={value!r}")
    if isinstance(value, (np.floating,)):
        float_value = float(value)
        if math.isnan(float_value):
            return None
        if float_value == 1.0:
            return True
        if float_value == 0.0:
            return False
        raise ValueError(f"invalid_boolean_value_for_{column}={value!r}")
    if isinstance(value, (bool, np.bool_)):
        return bool(value)
    if isinstance(value, (int, np.integer)):
        if int(value) == 1:
            return True
        if int(value) == 0:
            return False
        raise ValueError(f"invalid_boolean_value_for_{column}={value!r}")
    raise ValueError(f"invalid_boolean_value_for_{column}={value!r}")


def normalize_value_for_postgres(value: Any) -> Any:
    if value is None:
        return None
    if value is pd.NA or value is pd.NaT:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, (np.floating,)):
        float_value = float(value)
        return None if math.isnan(float_value) else float_value
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, pd.Timestamp):
        if pd.isna(value):
            return None
        if value.tzinfo is None:
            return value.to_pydatetime().replace(tzinfo=timezone.utc)
        return value.tz_convert("UTC").to_pydatetime()
    if isinstance(value, datetime):
        return _as_utc_timestamp(value).to_pydatetime()
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return json.dumps(_normalize_json(value), sort_keys=True)
    if isinstance(value, (list, tuple)):
        return [_normalize_json(item) for item in value]
    if isinstance(value, Decimal):
        return float(value)
    return value


def _quality_record_from_integrated(
    run_id: str | UUID,
    result: dict[str, Any],
) -> dict[str, Any]:
    blocking_errors = list(result.get("blocking_errors") or [])
    warnings = list(result.get("warnings") or [])
    rows_checked = int(result.get("rows_checked") or 0)
    rows_failed = rows_checked if blocking_errors else 0
    return {
        "run_id": str(run_id),
        "check_name": "integrated",
        "check_status": result.get("status", "failed"),
        "severity": "blocking" if blocking_errors else "info",
        "rows_checked": rows_checked,
        "rows_failed": rows_failed,
        "nulls_found": _integrated_null_count(result),
        "infinities_found": int(result.get("infinite_count") or 0),
        "duplicates_found": int(result.get("duplicate_count") or 0),
        "lookahead_violations": 0,
        "data_quality_score": result.get("data_quality_score"),
        "error_message": "; ".join(blocking_errors) if blocking_errors else None,
        "metadata": {
            "ready_for_storage": bool(result.get("ready_for_storage")),
            "warnings": warnings,
            "missing_columns": list(result.get("missing_columns") or []),
            "unexpected_columns": list(result.get("unexpected_columns") or []),
            "forbidden_columns_found": list(
                result.get("forbidden_columns_found") or []
            ),
        },
    }


def _quality_record_from_family(
    run_id: str | UUID,
    family_name: str,
    result: dict[str, Any],
) -> dict[str, Any]:
    errors = list(result.get("errors") or [])
    rows_checked = int(result.get("rows_checked") or 0)
    return {
        "run_id": str(run_id),
        "check_name": family_name,
        "check_status": result.get("status", "failed"),
        "severity": "blocking" if errors else "info",
        "rows_checked": rows_checked,
        "rows_failed": rows_checked if errors else 0,
        "nulls_found": 0,
        "infinities_found": 0,
        "duplicates_found": 0,
        "lookahead_violations": 0,
        "data_quality_score": None,
        "error_message": "; ".join(errors) if errors else None,
        "metadata": {
            "passed": bool(result.get("passed")),
            "warnings": list(result.get("warnings") or []),
        },
    }


def _integrated_null_count(result: dict[str, Any]) -> int:
    null_counts = result.get("null_counts_by_family") or {}
    total = 0
    for family_counts in null_counts.values():
        if isinstance(family_counts, dict):
            total += sum(int(value or 0) for value in family_counts.values())
    return total


def _run_completion_metadata(
    integrated_quality_result: dict[str, Any],
    parquet_paths: list[str | Path] | None,
) -> dict[str, Any]:
    return {
        "data_quality_score": integrated_quality_result.get("data_quality_score"),
        "ready_for_storage": bool(integrated_quality_result.get("ready_for_storage")),
        "parquet_paths": [str(path) for path in (parquet_paths or [])],
    }


def _as_utc_timestamp(value: datetime) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        return timestamp.tz_localize("UTC")
    return timestamp.tz_convert("UTC")


def _normalize_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _normalize_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize_json(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, pd.Timestamp):
        normalized_timestamp = normalize_value_for_postgres(value)
        return normalized_timestamp.isoformat() if normalized_timestamp else None
    if isinstance(value, datetime):
        return _as_utc_timestamp(value).isoformat()
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        float_value = float(value)
        return None if math.isnan(float_value) else float_value
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, float) and math.isnan(value):
        return None
    if value is pd.NA or value is pd.NaT:
        return None
    return value
