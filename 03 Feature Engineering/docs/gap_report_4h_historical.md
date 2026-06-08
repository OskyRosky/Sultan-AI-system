# Historical 4h Gap Report - technical_v1 / 1.0.0

## Scope

This report documents historical 4h OHLCV gaps observed during the production feature generation run:

```text
run_id = 5faf4e40-0087-4a63-95fe-03e9d11a3271
feature_set = technical_v1
feature_version = 1.0.0
generated_at = 2026-06-08
```

The gaps existed in `public.ohlcv_curated` before feature generation. They were not introduced by `03 Feature Engineering`.

## Interpretation

- The gaps affect `BTCUSDT 4h` and `ETHUSDT 4h`.
- The same 8 historical gaps apply to both 4h series.
- `BTCUSDT 1d` and `ETHUSDT 1d` have `gap_count = 0` for this report.
- No missing data was imputed, filled, forward-filled, or synthesized.
- These gaps are warnings, not blocking errors for feature generation.
- `06 Backtesting Engine` must be gap-aware and handle transitions across these gaps explicitly.

## Gap Summary

| # | gap_start_utc_minus_6 | gap_end_utc_minus_6 | delta | missing_4h_bars |
|---:|---|---|---|---:|
| 1 | 2018-02-07 18:00 | 2018-02-09 02:00 | 1d 8h | 8 |
| 2 | 2018-06-25 18:00 | 2018-06-26 06:00 | 12h | 3 |
| 3 | 2018-07-03 18:00 | 2018-07-04 02:00 | 8h | 2 |
| 4 | 2018-11-13 18:00 | 2018-11-14 02:00 | 8h | 2 |
| 5 | 2019-03-11 18:00 | 2019-03-12 02:00 | 8h | 2 |
| 6 | 2019-05-14 18:00 | 2019-05-15 06:00 | 12h | 3 |
| 7 | 2019-08-14 18:00 | 2019-08-15 02:00 | 8h | 2 |
| 8 | 2020-02-19 02:00 | 2020-02-19 10:00 | 8h | 2 |

## Series Status

```text
BTCUSDT 4h gap_count = 8
ETHUSDT 4h gap_count = 8
BTCUSDT 1d gap_count = 0
ETHUSDT 1d gap_count = 0
```

This report is a formal warning artifact for downstream consumers. It does not declare backtesting readiness.
