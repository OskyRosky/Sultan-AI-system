"""Feature quality checks for feature preview data."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd


RETURN_FEATURE_COLUMNS = ["simple_return", "log_return", "close_open_return"]
TREND_FEATURE_COLUMNS = [
    "sma_20",
    "sma_50",
    "ema_20",
    "ema_50",
    "price_above_sma20",
    "sma20_slope",
    "ema20_above_ema50",
]
TREND_NUMERIC_COLUMNS = ["sma_20", "sma_50", "ema_20", "ema_50", "sma20_slope"]
TREND_STATE_COLUMNS = ["price_above_sma20", "ema20_above_ema50"]
VOLATILITY_FEATURE_COLUMNS = ["rolling_std_20", "volatility_20", "atr_14"]
MOMENTUM_FEATURE_COLUMNS = ["rsi_14", "macd", "macd_signal"]
BREAKOUT_CONTEXT_FEATURE_COLUMNS = [
    "close_vs_high_52w",
    "rolling_max_20",
    "rolling_min_20",
]
VOLUME_FEATURE_COLUMNS = ["volume_change", "volume_sma_20", "volume_ratio_20"]
CANDLE_STRUCTURE_FEATURE_COLUMNS = [
    "high_low_range",
    "body_size",
    "upper_wick",
    "lower_wick",
    "body_to_range_ratio",
]
HIGH_52W_LOOKBACK_BY_TIMEFRAME = {
    "1d": 365,
    "4h": 2190,
}
FEATURE_KEY_COLUMNS = [
    "exchange",
    "symbol",
    "timeframe",
    "timestamp",
    "feature_set",
    "feature_version",
]
FORBIDDEN_COLUMNS = [
    "signal",
    "buy_signal",
    "sell_signal",
    "position",
    "entry",
    "exit",
    "pnl",
    "strategy_return",
    "backtest_return",
    "cross",
    "crossover",
    "golden_cross",
    "death_cross",
    "rsi_signal",
    "macd_cross",
    "macd_signal_cross",
    "macd_crossover",
    "breakout_signal",
    "breakout",
    "support",
    "resistance",
    "high_breakout",
    "low_breakdown",
    "volume_signal",
    "volume_spike_signal",
    "candle_signal",
    "doji_signal",
    "hammer_signal",
    "engulfing_signal",
]


def validate_return_features(df: pd.DataFrame) -> dict[str, Any]:
    """Validate return features without writing audit records."""

    errors: list[str] = []
    warnings: list[str] = []

    missing_return_columns = [
        column for column in RETURN_FEATURE_COLUMNS if column not in df.columns
    ]
    if missing_return_columns:
        errors.append(f"missing_return_columns={missing_return_columns}")

    forbidden_present = [column for column in FORBIDDEN_COLUMNS if column in df.columns]
    if forbidden_present:
        errors.append(f"forbidden_columns={forbidden_present}")

    missing_key_columns = [column for column in FEATURE_KEY_COLUMNS if column not in df.columns]
    if missing_key_columns:
        errors.append(f"missing_feature_key_columns={missing_key_columns}")

    if errors:
        return _result(False, len(df), errors, warnings)

    if df.empty:
        errors.append("empty_feature_dataframe")
        return _result(False, 0, errors, warnings)

    working = df.copy()
    working["timestamp"] = pd.to_datetime(working["timestamp"], utc=True, errors="coerce")
    if working["timestamp"].isna().any():
        errors.append("timestamp_null_or_invalid")

    if working["feature_set"].isna().any() or (working["feature_set"] == "").any():
        errors.append("feature_set_null_or_empty")
    if working["feature_version"].isna().any() or (
        working["feature_version"] == ""
    ).any():
        errors.append("feature_version_null_or_empty")

    duplicate_count = working.duplicated(subset=FEATURE_KEY_COLUMNS).sum()
    if duplicate_count:
        errors.append(f"duplicate_feature_rows={int(duplicate_count)}")

    for column in RETURN_FEATURE_COLUMNS:
        values = pd.to_numeric(working[column], errors="coerce")
        if np.isinf(values).any():
            errors.append(f"{column}_contains_infinite")

    _validate_return_nans(working, errors, warnings)

    return _result(not errors, len(df), errors, warnings)


def validate_trend_features(df: pd.DataFrame) -> dict[str, Any]:
    """Validate trend features without writing audit records."""

    errors: list[str] = []
    warnings: list[str] = []

    missing_trend_columns = [
        column for column in TREND_FEATURE_COLUMNS if column not in df.columns
    ]
    if missing_trend_columns:
        errors.append(f"missing_trend_columns={missing_trend_columns}")

    forbidden_present = [column for column in FORBIDDEN_COLUMNS if column in df.columns]
    if forbidden_present:
        errors.append(f"forbidden_columns={forbidden_present}")

    missing_key_columns = [column for column in FEATURE_KEY_COLUMNS if column not in df.columns]
    if missing_key_columns:
        errors.append(f"missing_feature_key_columns={missing_key_columns}")

    if errors:
        return _result(False, len(df), errors, warnings)

    if df.empty:
        errors.append("empty_feature_dataframe")
        return _result(False, 0, errors, warnings)

    working = df.copy()
    working["timestamp"] = pd.to_datetime(working["timestamp"], utc=True, errors="coerce")
    if working["timestamp"].isna().any():
        errors.append("timestamp_null_or_invalid")

    if working["feature_set"].isna().any() or (working["feature_set"] == "").any():
        errors.append("feature_set_null_or_empty")
    if working["feature_version"].isna().any() or (
        working["feature_version"] == ""
    ).any():
        errors.append("feature_version_null_or_empty")

    duplicate_count = working.duplicated(subset=FEATURE_KEY_COLUMNS).sum()
    if duplicate_count:
        errors.append(f"duplicate_feature_rows={int(duplicate_count)}")

    for column in TREND_NUMERIC_COLUMNS:
        values = pd.to_numeric(working[column], errors="coerce")
        if np.isinf(values).any():
            errors.append(f"{column}_contains_infinite")

    for column in TREND_STATE_COLUMNS:
        invalid_count = _invalid_state_count(working[column])
        if invalid_count:
            errors.append(f"{column}_invalid_state_values={invalid_count}")

    _validate_trend_nans(working, errors, warnings)

    return _result(not errors, len(df), errors, warnings)


def validate_volatility_features(df: pd.DataFrame) -> dict[str, Any]:
    """Validate volatility features without writing audit records."""

    errors: list[str] = []
    warnings: list[str] = []

    missing_volatility_columns = [
        column for column in VOLATILITY_FEATURE_COLUMNS if column not in df.columns
    ]
    if missing_volatility_columns:
        errors.append(f"missing_volatility_columns={missing_volatility_columns}")

    forbidden_present = [column for column in FORBIDDEN_COLUMNS if column in df.columns]
    if forbidden_present:
        errors.append(f"forbidden_columns={forbidden_present}")

    missing_key_columns = [column for column in FEATURE_KEY_COLUMNS if column not in df.columns]
    if missing_key_columns:
        errors.append(f"missing_feature_key_columns={missing_key_columns}")

    if errors:
        return _result(False, len(df), errors, warnings)

    if df.empty:
        errors.append("empty_feature_dataframe")
        return _result(False, 0, errors, warnings)

    working = df.copy()
    working["timestamp"] = pd.to_datetime(working["timestamp"], utc=True, errors="coerce")
    if working["timestamp"].isna().any():
        errors.append("timestamp_null_or_invalid")

    if working["feature_set"].isna().any() or (working["feature_set"] == "").any():
        errors.append("feature_set_null_or_empty")
    if working["feature_version"].isna().any() or (
        working["feature_version"] == ""
    ).any():
        errors.append("feature_version_null_or_empty")

    duplicate_count = working.duplicated(subset=FEATURE_KEY_COLUMNS).sum()
    if duplicate_count:
        errors.append(f"duplicate_feature_rows={int(duplicate_count)}")

    for column in VOLATILITY_FEATURE_COLUMNS:
        values = pd.to_numeric(working[column], errors="coerce")
        if np.isinf(values).any():
            errors.append(f"{column}_contains_infinite")
        if (values.dropna() < 0).any():
            errors.append(f"{column}_contains_negative")

    comparable = working[["rolling_std_20", "volatility_20"]].dropna()
    if not comparable.empty and not np.isclose(
        comparable["rolling_std_20"], comparable["volatility_20"]
    ).all():
        errors.append("volatility_20_not_equal_rolling_std_20")

    _validate_volatility_nans(working, errors, warnings)

    return _result(not errors, len(df), errors, warnings)


def validate_momentum_features(df: pd.DataFrame) -> dict[str, Any]:
    """Validate momentum features without writing audit records."""

    errors: list[str] = []
    warnings: list[str] = []

    missing_momentum_columns = [
        column for column in MOMENTUM_FEATURE_COLUMNS if column not in df.columns
    ]
    if missing_momentum_columns:
        errors.append(f"missing_momentum_columns={missing_momentum_columns}")

    forbidden_present = [column for column in FORBIDDEN_COLUMNS if column in df.columns]
    if forbidden_present:
        errors.append(f"forbidden_columns={forbidden_present}")

    missing_key_columns = [column for column in FEATURE_KEY_COLUMNS if column not in df.columns]
    if missing_key_columns:
        errors.append(f"missing_feature_key_columns={missing_key_columns}")

    if errors:
        return _result(False, len(df), errors, warnings)

    if df.empty:
        errors.append("empty_feature_dataframe")
        return _result(False, 0, errors, warnings)

    working = df.copy()
    working["timestamp"] = pd.to_datetime(working["timestamp"], utc=True, errors="coerce")
    if working["timestamp"].isna().any():
        errors.append("timestamp_null_or_invalid")

    if working["feature_set"].isna().any() or (working["feature_set"] == "").any():
        errors.append("feature_set_null_or_empty")
    if working["feature_version"].isna().any() or (
        working["feature_version"] == ""
    ).any():
        errors.append("feature_version_null_or_empty")

    duplicate_count = working.duplicated(subset=FEATURE_KEY_COLUMNS).sum()
    if duplicate_count:
        errors.append(f"duplicate_feature_rows={int(duplicate_count)}")

    for column in MOMENTUM_FEATURE_COLUMNS:
        values = pd.to_numeric(working[column], errors="coerce")
        if np.isinf(values).any():
            errors.append(f"{column}_contains_infinite")

    rsi = pd.to_numeric(working["rsi_14"], errors="coerce")
    if ((rsi.dropna() < 0) | (rsi.dropna() > 100)).any():
        errors.append("rsi_14_out_of_range")

    _validate_momentum_nans(working, errors, warnings)

    return _result(not errors, len(df), errors, warnings)


def validate_breakout_context_features(df: pd.DataFrame) -> dict[str, Any]:
    """Validate breakout context features without writing audit records."""

    errors: list[str] = []
    warnings: list[str] = []

    missing_breakout_columns = [
        column for column in BREAKOUT_CONTEXT_FEATURE_COLUMNS if column not in df.columns
    ]
    if missing_breakout_columns:
        errors.append(f"missing_breakout_context_columns={missing_breakout_columns}")

    forbidden_present = [column for column in FORBIDDEN_COLUMNS if column in df.columns]
    if forbidden_present:
        errors.append(f"forbidden_columns={forbidden_present}")

    missing_key_columns = [column for column in FEATURE_KEY_COLUMNS if column not in df.columns]
    if missing_key_columns:
        errors.append(f"missing_feature_key_columns={missing_key_columns}")

    if errors:
        return _result(False, len(df), errors, warnings)

    if df.empty:
        errors.append("empty_feature_dataframe")
        return _result(False, 0, errors, warnings)

    working = df.copy()
    working["timestamp"] = pd.to_datetime(working["timestamp"], utc=True, errors="coerce")
    if working["timestamp"].isna().any():
        errors.append("timestamp_null_or_invalid")

    if working["feature_set"].isna().any() or (working["feature_set"] == "").any():
        errors.append("feature_set_null_or_empty")
    if working["feature_version"].isna().any() or (
        working["feature_version"] == ""
    ).any():
        errors.append("feature_version_null_or_empty")

    duplicate_count = working.duplicated(subset=FEATURE_KEY_COLUMNS).sum()
    if duplicate_count:
        errors.append(f"duplicate_feature_rows={int(duplicate_count)}")

    for column in BREAKOUT_CONTEXT_FEATURE_COLUMNS:
        values = pd.to_numeric(working[column], errors="coerce")
        if np.isinf(values).any():
            errors.append(f"{column}_contains_infinite")
        if (values.dropna() < 0).any():
            errors.append(f"{column}_contains_negative")

    _validate_breakout_context_nans(working, errors, warnings)

    return _result(not errors, len(df), errors, warnings)


def validate_volume_features(df: pd.DataFrame) -> dict[str, Any]:
    """Validate volume features without writing audit records."""

    errors: list[str] = []
    warnings: list[str] = []

    missing_volume_columns = [
        column for column in VOLUME_FEATURE_COLUMNS if column not in df.columns
    ]
    if missing_volume_columns:
        errors.append(f"missing_volume_columns={missing_volume_columns}")

    forbidden_present = [column for column in FORBIDDEN_COLUMNS if column in df.columns]
    if forbidden_present:
        errors.append(f"forbidden_columns={forbidden_present}")

    missing_key_columns = [column for column in FEATURE_KEY_COLUMNS if column not in df.columns]
    if missing_key_columns:
        errors.append(f"missing_feature_key_columns={missing_key_columns}")

    if errors:
        return _result(False, len(df), errors, warnings)

    if df.empty:
        errors.append("empty_feature_dataframe")
        return _result(False, 0, errors, warnings)

    working = df.copy()
    working["timestamp"] = pd.to_datetime(working["timestamp"], utc=True, errors="coerce")
    if working["timestamp"].isna().any():
        errors.append("timestamp_null_or_invalid")

    if working["feature_set"].isna().any() or (working["feature_set"] == "").any():
        errors.append("feature_set_null_or_empty")
    if working["feature_version"].isna().any() or (
        working["feature_version"] == ""
    ).any():
        errors.append("feature_version_null_or_empty")

    duplicate_count = working.duplicated(subset=FEATURE_KEY_COLUMNS).sum()
    if duplicate_count:
        errors.append(f"duplicate_feature_rows={int(duplicate_count)}")

    for column in VOLUME_FEATURE_COLUMNS:
        values = pd.to_numeric(working[column], errors="coerce")
        if np.isinf(values).any():
            errors.append(f"{column}_contains_infinite")

    for column in ["volume_sma_20", "volume_ratio_20"]:
        values = pd.to_numeric(working[column], errors="coerce")
        if (values.dropna() < 0).any():
            errors.append(f"{column}_contains_negative")

    _validate_volume_nans(working, errors, warnings)

    return _result(not errors, len(df), errors, warnings)


def validate_candle_structure_features(df: pd.DataFrame) -> dict[str, Any]:
    """Validate candle structure features without writing audit records."""

    errors: list[str] = []
    warnings: list[str] = []

    missing_candle_columns = [
        column for column in CANDLE_STRUCTURE_FEATURE_COLUMNS if column not in df.columns
    ]
    if missing_candle_columns:
        errors.append(f"missing_candle_structure_columns={missing_candle_columns}")

    forbidden_present = [column for column in FORBIDDEN_COLUMNS if column in df.columns]
    if forbidden_present:
        errors.append(f"forbidden_columns={forbidden_present}")

    missing_key_columns = [column for column in FEATURE_KEY_COLUMNS if column not in df.columns]
    if missing_key_columns:
        errors.append(f"missing_feature_key_columns={missing_key_columns}")

    if errors:
        return _result(False, len(df), errors, warnings)

    if df.empty:
        errors.append("empty_feature_dataframe")
        return _result(False, 0, errors, warnings)

    working = df.copy()
    working["timestamp"] = pd.to_datetime(working["timestamp"], utc=True, errors="coerce")
    if working["timestamp"].isna().any():
        errors.append("timestamp_null_or_invalid")

    if working["feature_set"].isna().any() or (working["feature_set"] == "").any():
        errors.append("feature_set_null_or_empty")
    if working["feature_version"].isna().any() or (
        working["feature_version"] == ""
    ).any():
        errors.append("feature_version_null_or_empty")

    duplicate_count = working.duplicated(subset=FEATURE_KEY_COLUMNS).sum()
    if duplicate_count:
        errors.append(f"duplicate_feature_rows={int(duplicate_count)}")

    for column in CANDLE_STRUCTURE_FEATURE_COLUMNS:
        values = pd.to_numeric(working[column], errors="coerce")
        if np.isinf(values).any():
            errors.append(f"{column}_contains_infinite")

    for column in ["high_low_range", "body_size", "upper_wick", "lower_wick"]:
        values = pd.to_numeric(working[column], errors="coerce")
        if (values.dropna() < 0).any():
            errors.append(f"{column}_contains_negative")

    ratio = pd.to_numeric(working["body_to_range_ratio"], errors="coerce")
    if ((ratio.dropna() < 0) | (ratio.dropna() > 1)).any():
        errors.append("body_to_range_ratio_out_of_range")

    _validate_candle_structure_nans(working, errors, warnings)

    return _result(not errors, len(df), errors, warnings)


def _validate_return_nans(
    df: pd.DataFrame, errors: list[str], warnings: list[str]
) -> None:
    sorted_df = df.sort_values(["exchange", "symbol", "timeframe", "timestamp"]).copy()
    first_row_mask = (
        sorted_df.groupby(["exchange", "symbol", "timeframe"], sort=False)
        .cumcount()
        .eq(0)
    )

    open_positive = pd.to_numeric(sorted_df["open"], errors="coerce") > 0
    close_positive = pd.to_numeric(sorted_df["close"], errors="coerce") > 0

    previous_close = sorted_df.groupby(
        ["exchange", "symbol", "timeframe"], sort=False
    )["close"].shift(1)
    previous_close_positive = pd.to_numeric(previous_close, errors="coerce") > 0

    simple_nan = sorted_df["simple_return"].isna()
    log_nan = sorted_df["log_return"].isna()
    close_open_nan = sorted_df["close_open_return"].isna()

    invalid_previous_context = first_row_mask | ~previous_close_positive | ~close_positive
    unexpected_simple_nan = simple_nan & ~invalid_previous_context
    unexpected_log_nan = log_nan & ~invalid_previous_context
    unexpected_close_open_nan = close_open_nan & open_positive & close_positive

    if unexpected_simple_nan.any():
        errors.append(f"simple_return_unexpected_nan={int(unexpected_simple_nan.sum())}")
    if unexpected_log_nan.any():
        errors.append(f"log_return_unexpected_nan={int(unexpected_log_nan.sum())}")
    if unexpected_close_open_nan.any():
        errors.append(
            f"close_open_return_unexpected_nan={int(unexpected_close_open_nan.sum())}"
        )

    invalid_price_rows = int((~open_positive | ~close_positive | ~previous_close_positive).sum())
    if invalid_price_rows:
        warnings.append(f"nan_allowed_for_invalid_price_context_rows={invalid_price_rows}")


def _validate_trend_nans(
    df: pd.DataFrame, errors: list[str], warnings: list[str]
) -> None:
    sorted_df = df.sort_values(["exchange", "symbol", "timeframe", "timestamp"]).copy()
    group_index = sorted_df.groupby(["exchange", "symbol", "timeframe"], sort=False).cumcount()
    close_available = sorted_df["close"].notna()

    unexpected_sma20_nan = sorted_df["sma_20"].isna() & group_index.ge(19)
    unexpected_sma50_nan = sorted_df["sma_50"].isna() & group_index.ge(49)
    unexpected_sma20_slope_nan = sorted_df["sma20_slope"].isna() & group_index.ge(20)
    unexpected_price_state_nan = (
        sorted_df["price_above_sma20"].isna() & sorted_df["sma_20"].notna()
    )
    unexpected_ema20_nan = sorted_df["ema_20"].isna() & close_available
    unexpected_ema50_nan = sorted_df["ema_50"].isna() & close_available

    if unexpected_sma20_nan.any():
        errors.append(f"sma_20_unexpected_nan={int(unexpected_sma20_nan.sum())}")
    if unexpected_sma50_nan.any():
        errors.append(f"sma_50_unexpected_nan={int(unexpected_sma50_nan.sum())}")
    if unexpected_sma20_slope_nan.any():
        errors.append(
            f"sma20_slope_unexpected_nan={int(unexpected_sma20_slope_nan.sum())}"
        )
    if unexpected_price_state_nan.any():
        errors.append(
            "price_above_sma20_unexpected_nan="
            f"{int(unexpected_price_state_nan.sum())}"
        )
    if unexpected_ema20_nan.any():
        errors.append(f"ema_20_unexpected_nan={int(unexpected_ema20_nan.sum())}")
    if unexpected_ema50_nan.any():
        errors.append(f"ema_50_unexpected_nan={int(unexpected_ema50_nan.sum())}")

    warmup_rows = int(group_index.lt(49).sum())
    if warmup_rows:
        warnings.append(f"trend_warmup_rows={warmup_rows}")


def _invalid_state_count(series: pd.Series) -> int:
    non_null = series.dropna()
    if non_null.empty:
        return 0
    valid_values = {True, False, 0, 1, 0.0, 1.0}
    return int((~non_null.map(lambda value: value in valid_values)).sum())


def _validate_volatility_nans(
    df: pd.DataFrame, errors: list[str], warnings: list[str]
) -> None:
    sorted_df = df.sort_values(["exchange", "symbol", "timeframe", "timestamp"]).copy()
    group_index = sorted_df.groupby(["exchange", "symbol", "timeframe"], sort=False).cumcount()

    unexpected_rolling_std_nan = sorted_df["rolling_std_20"].isna() & group_index.ge(20)
    unexpected_volatility_nan = (
        sorted_df["volatility_20"].isna() & sorted_df["rolling_std_20"].notna()
    )
    unexpected_atr_nan = sorted_df["atr_14"].isna() & group_index.ge(13)

    if unexpected_rolling_std_nan.any():
        errors.append(
            f"rolling_std_20_unexpected_nan={int(unexpected_rolling_std_nan.sum())}"
        )
    if unexpected_volatility_nan.any():
        errors.append(
            f"volatility_20_unexpected_nan={int(unexpected_volatility_nan.sum())}"
        )
    if unexpected_atr_nan.any():
        errors.append(f"atr_14_unexpected_nan={int(unexpected_atr_nan.sum())}")

    warmup_rows = int(group_index.lt(20).sum())
    if warmup_rows:
        warnings.append(f"volatility_warmup_rows={warmup_rows}")


def _validate_momentum_nans(
    df: pd.DataFrame, errors: list[str], warnings: list[str]
) -> None:
    sorted_df = df.sort_values(["exchange", "symbol", "timeframe", "timestamp"]).copy()
    group_index = sorted_df.groupby(["exchange", "symbol", "timeframe"], sort=False).cumcount()
    close_available = sorted_df["close"].notna()

    unexpected_rsi_nan = sorted_df["rsi_14"].isna() & group_index.ge(14)
    unexpected_macd_nan = sorted_df["macd"].isna() & close_available
    unexpected_macd_signal_nan = sorted_df["macd_signal"].isna() & close_available

    if unexpected_rsi_nan.any():
        errors.append(f"rsi_14_unexpected_nan={int(unexpected_rsi_nan.sum())}")
    if unexpected_macd_nan.any():
        errors.append(f"macd_unexpected_nan={int(unexpected_macd_nan.sum())}")
    if unexpected_macd_signal_nan.any():
        errors.append(
            f"macd_signal_unexpected_nan={int(unexpected_macd_signal_nan.sum())}"
        )

    warmup_rows = int(group_index.lt(14).sum())
    if warmup_rows:
        warnings.append(f"momentum_warmup_rows={warmup_rows}")


def _validate_breakout_context_nans(
    df: pd.DataFrame, errors: list[str], warnings: list[str]
) -> None:
    sorted_df = df.sort_values(["exchange", "symbol", "timeframe", "timestamp"]).copy()
    group_index = sorted_df.groupby(["exchange", "symbol", "timeframe"], sort=False).cumcount()

    unexpected_rolling_max_nan = sorted_df["rolling_max_20"].isna() & group_index.ge(19)
    unexpected_rolling_min_nan = sorted_df["rolling_min_20"].isna() & group_index.ge(19)

    if unexpected_rolling_max_nan.any():
        errors.append(
            f"rolling_max_20_unexpected_nan={int(unexpected_rolling_max_nan.sum())}"
        )
    if unexpected_rolling_min_nan.any():
        errors.append(
            f"rolling_min_20_unexpected_nan={int(unexpected_rolling_min_nan.sum())}"
        )

    close_vs_high_nan = sorted_df["close_vs_high_52w"].isna()
    warmup_rows = 0
    for (_, _, timeframe), group in sorted_df.groupby(
        ["exchange", "symbol", "timeframe"], sort=False
    ):
        lookback = HIGH_52W_LOOKBACK_BY_TIMEFRAME.get(str(timeframe))
        if lookback is None:
            errors.append(f"unsupported_timeframe_for_close_vs_high_52w={timeframe}")
            continue
        local_index = pd.Series(np.arange(len(group)), index=group.index)
        warmup_mask = local_index.lt(lookback - 1)
        warmup_rows += int(warmup_mask.sum())
        unexpected_nan = close_vs_high_nan.loc[group.index] & ~warmup_mask
        if unexpected_nan.any():
            errors.append(
                "close_vs_high_52w_unexpected_nan="
                f"{int(unexpected_nan.sum())}"
            )

    if warmup_rows:
        warnings.append(f"breakout_context_warmup_rows={warmup_rows}")


def _validate_volume_nans(
    df: pd.DataFrame, errors: list[str], warnings: list[str]
) -> None:
    sorted_df = df.sort_values(["exchange", "symbol", "timeframe", "timestamp"]).copy()
    group_index = sorted_df.groupby(["exchange", "symbol", "timeframe"], sort=False).cumcount()

    previous_volume = sorted_df.groupby(["exchange", "symbol", "timeframe"], sort=False)[
        "volume"
    ].shift(1)
    previous_volume_positive = pd.to_numeric(previous_volume, errors="coerce") > 0

    unexpected_volume_change_nan = (
        sorted_df["volume_change"].isna() & group_index.gt(0) & previous_volume_positive
    )
    unexpected_volume_sma_nan = sorted_df["volume_sma_20"].isna() & group_index.ge(19)
    unexpected_volume_ratio_nan = (
        sorted_df["volume_ratio_20"].isna() & sorted_df["volume_sma_20"].gt(0)
    )

    if unexpected_volume_change_nan.any():
        errors.append(
            f"volume_change_unexpected_nan={int(unexpected_volume_change_nan.sum())}"
        )
    if unexpected_volume_sma_nan.any():
        errors.append(f"volume_sma_20_unexpected_nan={int(unexpected_volume_sma_nan.sum())}")
    if unexpected_volume_ratio_nan.any():
        errors.append(
            f"volume_ratio_20_unexpected_nan={int(unexpected_volume_ratio_nan.sum())}"
        )

    warmup_rows = int(group_index.lt(19).sum())
    if warmup_rows:
        warnings.append(f"volume_warmup_rows={warmup_rows}")


def _validate_candle_structure_nans(
    df: pd.DataFrame, errors: list[str], warnings: list[str]
) -> None:
    high_low_range = pd.to_numeric(df["high_low_range"], errors="coerce")
    ratio_nan = df["body_to_range_ratio"].isna()

    unexpected_ratio_nan = ratio_nan & high_low_range.gt(0)
    if unexpected_ratio_nan.any():
        errors.append(
            "body_to_range_ratio_unexpected_nan="
            f"{int(unexpected_ratio_nan.sum())}"
        )

    invalid_range_rows = int(high_low_range.le(0).sum())
    if invalid_range_rows:
        warnings.append(f"body_to_range_ratio_nan_allowed_rows={invalid_range_rows}")


def _result(
    passed: bool, rows_checked: int, errors: list[str], warnings: list[str]
) -> dict[str, Any]:
    return {
        "status": "passed" if passed else "failed",
        "passed": passed,
        "errors": errors,
        "warnings": warnings,
        "rows_checked": rows_checked,
    }
