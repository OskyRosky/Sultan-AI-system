from __future__ import annotations

import inspect
import sys
from pathlib import Path

import pandas as pd
import pytest

FLOWS_DIR = Path(__file__).resolve().parents[1] / "flows"
if str(FLOWS_DIR) not in sys.path:
    sys.path.insert(0, str(FLOWS_DIR))

import generate_features_flow as flow_module


def _patch_pipeline(monkeypatch: pytest.MonkeyPatch, ready_for_storage: bool = True) -> dict:
    calls = {
        "prepare": 0,
        "parquet": 0,
        "postgres": 0,
        "stop": 0,
    }
    frame = pd.DataFrame(
        {
            "symbol": ["BTCUSDT", "BTCUSDT"],
            "timeframe": ["1d", "1d"],
            "timestamp": pd.to_datetime(
                ["2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z"]
            ),
        }
    )

    def fake_config(
        symbols=None,
        timeframes=None,
        limit=1000,
        read_from_db=True,
        enable_storage=False,
        enable_parquet=True,
        enable_postgres=True,
        require_freshness=True,
        allow_full_history=False,
    ):
        flow_module._validate_flow_controls(
            read_from_db=read_from_db,
            enable_storage=enable_storage,
            limit=limit,
            allow_full_history=allow_full_history,
        )
        return {
            "run_id": "test-run",
            "flow_name": "generate_features_flow",
            "feature_set": "technical_v1",
            "feature_version": "1.0.0",
            "symbols": symbols or ["BTCUSDT"],
            "timeframes": timeframes or ["1d"],
            "created_at": "2026-05-17T12:00:00+00:00",
            "mode": "controlled_storage" if enable_storage else "controlled_preview",
            "read_from_db": read_from_db,
            "limit": limit,
            "enable_storage": enable_storage,
            "enable_parquet": enable_parquet,
            "enable_postgres": enable_postgres,
            "require_freshness": require_freshness,
            "allow_full_history": allow_full_history,
            "ohlcv_table": "public.ohlcv_curated",
        }

    family_result = {"status": "passed", "passed": True, "rows_checked": 2, "errors": [], "warnings": []}
    integrated_result = {
        "status": "passed" if ready_for_storage else "failed",
        "ready_for_storage": ready_for_storage,
        "data_quality_score": 1.0 if ready_for_storage else 0.5,
        "rows_checked": 2,
        "blocking_errors": [] if ready_for_storage else ["forced_failure"],
        "warnings": [],
    }

    monkeypatch.setattr(flow_module, "load_feature_config", fake_config)
    monkeypatch.setattr(flow_module, "check_ohlcv_freshness", lambda config: [{"passed": True}])
    monkeypatch.setattr(flow_module, "load_ohlcv_data_read_only", lambda config: frame)
    monkeypatch.setattr(flow_module, "validate_ohlcv_data", lambda df: {"passed": True, "rows_checked": len(df)})
    monkeypatch.setattr(flow_module, "calculate_returns_features_preview", lambda df: df)
    monkeypatch.setattr(flow_module, "calculate_trend_features_preview", lambda df: df)
    monkeypatch.setattr(flow_module, "calculate_volatility_features_preview", lambda df: df)
    monkeypatch.setattr(flow_module, "calculate_momentum_features_preview", lambda df: df)
    monkeypatch.setattr(flow_module, "calculate_breakout_context_features_preview", lambda df: df)
    monkeypatch.setattr(flow_module, "calculate_volume_features_preview", lambda df: df)
    monkeypatch.setattr(flow_module, "calculate_candle_structure_features_preview", lambda df: df)
    monkeypatch.setattr(flow_module, "validate_returns_features_preview", lambda df: family_result)
    monkeypatch.setattr(flow_module, "validate_trend_features_preview", lambda df: family_result)
    monkeypatch.setattr(flow_module, "validate_volatility_features_preview", lambda df: family_result)
    monkeypatch.setattr(flow_module, "validate_momentum_features_preview", lambda df: family_result)
    monkeypatch.setattr(flow_module, "validate_breakout_context_features_preview", lambda df: family_result)
    monkeypatch.setattr(flow_module, "validate_volume_features_preview", lambda df: family_result)
    monkeypatch.setattr(flow_module, "validate_candle_structure_features_preview", lambda df: family_result)
    monkeypatch.setattr(flow_module, "validate_integrated_feature_dataset_preview", lambda df: integrated_result)

    def fake_summary(*args):
        config = args[-1]
        return {
            "integrated_quality_status": integrated_result["status"],
            "integrated_ready_for_storage": integrated_result["ready_for_storage"],
            "integrated_data_quality_score": integrated_result["data_quality_score"],
            "enable_storage": config["enable_storage"],
        }

    def fake_stop(summary):
        calls["stop"] += 1
        return {
            "status": "stopped_before_persistence",
            "parquet_written": False,
            "postgres_inserted": False,
            "summary": summary,
        }

    def fake_prepare(features_df, config, integrated_quality_result):
        calls["prepare"] += 1
        return features_df

    def fake_parquet(storage_df, config):
        calls["parquet"] += 1
        return ["data/features/test.parquet"]

    def fake_postgres(*_args):
        calls["postgres"] += 1
        return {"status": "passed", "rows_inserted": 2, "features_upserted": True}

    monkeypatch.setattr(flow_module, "summarize_feature_preview", fake_summary)
    monkeypatch.setattr(flow_module, "stop_before_persistence", fake_stop)
    monkeypatch.setattr(flow_module, "prepare_features_for_storage_task", fake_prepare)
    monkeypatch.setattr(flow_module, "write_features_parquet_task", fake_parquet)
    monkeypatch.setattr(flow_module, "store_features_postgres_task", fake_postgres)
    monkeypatch.setattr(
        flow_module,
        "summarize_storage_result",
        lambda config, storage_df, parquet_paths, postgres_result: {
            "enabled": True,
            "parquet_paths": parquet_paths,
            "postgres": postgres_result,
        },
    )
    return calls


def test_flow_default_does_not_enable_storage() -> None:
    signature = inspect.signature(flow_module.generate_features_flow.fn)

    assert signature.parameters["enable_storage"].default is False
    assert signature.parameters["read_from_db"].default is True


def test_flow_blocks_full_history_when_limit_none_and_allow_full_history_false() -> None:
    with pytest.raises(ValueError, match="limit_none_requires_allow_full_history_true"):
        flow_module._validate_flow_controls(
            read_from_db=True,
            enable_storage=False,
            limit=None,
            allow_full_history=False,
        )


def test_flow_allows_full_history_only_when_explicit() -> None:
    flow_module._validate_flow_controls(
        read_from_db=True,
        enable_storage=False,
        limit=None,
        allow_full_history=True,
    )


def test_flow_enable_storage_requires_read_from_db() -> None:
    with pytest.raises(ValueError, match="enable_storage_requires_read_from_db_true"):
        flow_module._validate_flow_controls(
            read_from_db=False,
            enable_storage=True,
            limit=100,
            allow_full_history=False,
        )


def test_flow_does_not_call_storage_when_enable_storage_false(monkeypatch) -> None:
    calls = _patch_pipeline(monkeypatch, ready_for_storage=True)

    result = flow_module.generate_features_flow.fn(enable_storage=False, read_from_db=True)

    assert calls["prepare"] == 0
    assert calls["parquet"] == 0
    assert calls["postgres"] == 0
    assert result["stop"]["status"] == "stopped_before_persistence"


def test_flow_calls_storage_when_enable_storage_true_and_ready(monkeypatch) -> None:
    calls = _patch_pipeline(monkeypatch, ready_for_storage=True)

    result = flow_module.generate_features_flow.fn(enable_storage=True, read_from_db=True)

    assert calls["prepare"] == 1
    assert calls["parquet"] == 1
    assert calls["postgres"] == 1
    assert result["storage"]["enabled"] is True


def test_flow_does_not_write_when_ready_for_storage_false(monkeypatch) -> None:
    calls = _patch_pipeline(monkeypatch, ready_for_storage=False)

    result = flow_module.generate_features_flow.fn(enable_storage=True, read_from_db=True)

    assert calls["prepare"] == 0
    assert calls["parquet"] == 0
    assert calls["postgres"] == 0
    assert result["stop"]["status"] == "storage_blocked_by_quality_gate"


def test_flow_summary_contains_quality_result(monkeypatch) -> None:
    _patch_pipeline(monkeypatch, ready_for_storage=True)

    result = flow_module.generate_features_flow.fn(enable_storage=False, read_from_db=True)

    assert result["summary"]["integrated_quality_status"] == "passed"
    assert result["integrated_quality"]["data_quality_score"] == 1.0


def test_flow_summary_contains_storage_result_when_enabled(monkeypatch) -> None:
    _patch_pipeline(monkeypatch, ready_for_storage=True)

    result = flow_module.generate_features_flow.fn(enable_storage=True, read_from_db=True)

    assert result["storage"]["postgres"]["rows_inserted"] == 2
    assert result["storage"]["parquet_paths"] == ["data/features/test.parquet"]
