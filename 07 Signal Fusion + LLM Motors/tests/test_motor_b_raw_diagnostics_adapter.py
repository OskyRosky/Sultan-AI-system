from __future__ import annotations

from pathlib import Path
import sys

import pytest


STAGE07_SRC = Path(__file__).resolve().parents[1] / "src"
if str(STAGE07_SRC) not in sys.path:
    sys.path.insert(0, str(STAGE07_SRC))

from dry_run import default_mock_payload  # noqa: E402
from motor_b_adapter import adapt_motor_b_raw_diagnostics  # noqa: E402
from normalizer import normalize_motor_b  # noqa: E402


def _motor_b_payload() -> dict:
    return default_mock_payload()["motor_b"]


def test_motor_b_adapter_preserves_framework_only() -> None:
    adapted = adapt_motor_b_raw_diagnostics(_motor_b_payload())

    assert adapted.source_artifact_type == "RawDiagnosticsHandoffContract"
    assert adapted.evidence_completeness_level == "framework_only"
    assert adapted.empirical_results_available is False
    assert adapted.adapter_status == "accepted_for_dry_run_only"


def test_motor_b_adapter_preserves_confidence_null() -> None:
    adapted = adapt_motor_b_raw_diagnostics(_motor_b_payload())

    assert adapted.confidence_status == "confidence_not_available"
    assert adapted.confidence_score is None
    assert adapted.final_signal_confidence_score is None


def test_stage07_missing_required_fields_fail_closed() -> None:
    payload = _motor_b_payload()
    del payload["handoff_contract_id"]

    adapted = adapt_motor_b_raw_diagnostics(payload)

    assert adapted.adapter_status == "rejected_missing_required_fields_fail_closed"
    assert "missing_handoff_contract_id" in adapted.blocking_gaps
    assert adapted.paper_trading_ready is False
    assert adapted.handoff_to_09 == "blocked"


def test_stage07_forbidden_downstream_usage_present() -> None:
    adapted = adapt_motor_b_raw_diagnostics(_motor_b_payload())

    assert "paper_trading" in adapted.forbidden_downstream_usage
    assert "live_trading" in adapted.forbidden_downstream_usage
    assert "strategy_promotion" in adapted.forbidden_downstream_usage
    assert "confidence_generation" in adapted.forbidden_downstream_usage


def test_stage07_no_raw_stage06_without_contractual_adapter() -> None:
    raw_stage06 = _motor_b_payload()

    with pytest.raises(AttributeError):
        normalize_motor_b(raw_stage06)

