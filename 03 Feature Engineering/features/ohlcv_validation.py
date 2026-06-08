"""Read-only OHLCV DataFrame validation for feature readiness."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


REQUIRED_OHLCV_COLUMNS = [
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

NUMERIC_COLUMNS = ["open", "high", "low", "close", "volume"]
KEY_COLUMNS = ["exchange", "symbol", "timeframe", "timestamp"]
EXPECTED_TIMEFRAME_DELTAS = {
    "1d": pd.Timedelta(days=1),
    "4h": pd.Timedelta(hours=4),
}


@dataclass(frozen=True)
class OhlcvValidationResult:
    status: str
    passed: bool
    rows_checked: int
    errors: list[str]
    warnings: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "passed": self.passed,
            "rows_checked": self.rows_checked,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def validate_ohlcv_dataframe(df: pd.DataFrame) -> OhlcvValidationResult:
    """Validate minimum OHLCV structure without mutating the input DataFrame."""

    errors: list[str] = []
    warnings: list[str] = []

    if df.empty:
        errors.append("empty_dataframe")
        return OhlcvValidationResult("failed", False, 0, errors, warnings)

    missing_columns = [
        column for column in REQUIRED_OHLCV_COLUMNS if column not in df.columns
    ]
    if missing_columns:
        errors.append(f"missing_required_columns={missing_columns}")
        return OhlcvValidationResult("failed", False, len(df), errors, warnings)

    working = df[REQUIRED_OHLCV_COLUMNS].copy()

    for column in ["timestamp", "symbol", "timeframe", "exchange"]:
        if working[column].isna().any():
            errors.append(f"{column}_nulls")

    timestamp_values = pd.to_datetime(working["timestamp"], utc=True, errors="coerce")
    if timestamp_values.isna().any():
        errors.append("timestamp_not_convertible_to_datetime")
    else:
        working["timestamp"] = timestamp_values

    for column in NUMERIC_COLUMNS:
        numeric_values = pd.to_numeric(working[column], errors="coerce")
        if numeric_values.isna().any():
            errors.append(f"{column}_not_numeric_or_null")
        working[column] = numeric_values

    if errors:
        return OhlcvValidationResult("failed", False, len(df), errors, warnings)

    duplicate_count = working.duplicated(subset=KEY_COLUMNS).sum()
    if duplicate_count:
        errors.append(f"duplicate_bars={int(duplicate_count)}")

    if not _is_timestamp_ordered_by_group(working):
        errors.append("timestamp_not_ordered_by_symbol_timeframe")
    else:
        warnings.extend(detect_temporal_gaps(working))

    if (working["high"] < working["low"]).any():
        errors.append("high_lt_low")
    if (working["high"] < working["open"]).any():
        errors.append("high_lt_open")
    if (working["high"] < working["close"]).any():
        errors.append("high_lt_close")
    if (working["low"] > working["open"]).any():
        errors.append("low_gt_open")
    if (working["low"] > working["close"]).any():
        errors.append("low_gt_close")
    if (working["volume"] < 0).any():
        errors.append("volume_negative")

    passed = not errors
    return OhlcvValidationResult(
        status="passed" if passed else "failed",
        passed=passed,
        rows_checked=len(df),
        errors=errors,
        warnings=warnings,
    )


def _is_timestamp_ordered_by_group(df: pd.DataFrame) -> bool:
    for _, group in df.groupby(["symbol", "timeframe"], sort=False):
        if not group["timestamp"].is_monotonic_increasing:
            return False
    return True


def detect_temporal_gaps(df: pd.DataFrame) -> list[str]:
    """Report expected timeframe gaps without modifying or imputing OHLCV rows."""

    if df.empty:
        return []

    missing_columns = [column for column in KEY_COLUMNS if column not in df.columns]
    if missing_columns:
        return [f"gap_check_missing_key_columns={missing_columns}"]

    working = df.loc[:, KEY_COLUMNS].copy()
    working["timestamp"] = pd.to_datetime(working["timestamp"], utc=True, errors="coerce")
    if working["timestamp"].isna().any():
        return ["gap_check_timestamp_invalid"]

    warnings: list[str] = []
    group_columns = ["exchange", "symbol", "timeframe"]
    for (exchange, symbol, timeframe), group in working.groupby(group_columns, sort=False):
        expected_delta = EXPECTED_TIMEFRAME_DELTAS.get(str(timeframe))
        if expected_delta is None:
            warnings.append(
                "gap_check_unsupported_timeframe="
                f"{exchange}/{symbol}/{timeframe}"
            )
            continue

        ordered = group.sort_values("timestamp")
        observed_delta = ordered["timestamp"].diff()
        gap_mask = observed_delta.gt(expected_delta)
        if gap_mask.any():
            first_gap_index = gap_mask[gap_mask].index[0]
            previous_timestamp = ordered.loc[first_gap_index, "timestamp"] - observed_delta.loc[
                first_gap_index
            ]
            current_timestamp = ordered.loc[first_gap_index, "timestamp"]
            warnings.append(
                "temporal_gaps_detected="
                f"{exchange}/{symbol}/{timeframe}:"
                f"count={int(gap_mask.sum())}:"
                f"first_gap_after={previous_timestamp.isoformat()}:"
                f"first_gap_before={current_timestamp.isoformat()}"
            )

    return warnings
