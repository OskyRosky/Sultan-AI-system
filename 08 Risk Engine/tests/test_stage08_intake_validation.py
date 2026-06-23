from __future__ import annotations

from pathlib import Path
import sys

import pytest


STAGE08_SRC = Path(__file__).resolve().parents[1] / "src"
if str(STAGE08_SRC) not in sys.path:
    sys.path.insert(0, str(STAGE08_SRC))

from dry_run import default_stage07_risk_handoff_payload  # noqa: E402
from intake import Stage08IntakeError, validate_stage07_risk_handoff_package  # noqa: E402


def test_stage08_accepts_stage07_risk_handoff_package() -> None:
    payload = default_stage07_risk_handoff_payload()

    input_package = validate_stage07_risk_handoff_package(payload)

    assert input_package.source_stage == "07 Signal Fusion + LLM Motors"
    assert input_package.artifact_type == "RiskHandoffPackage"
    assert input_package.source_risk_handoff_package_id == payload["risk_handoff_package_id"]


def test_stage08_rejects_raw_stage06_artifact() -> None:
    payload = {
        "artifact_type": "Stage06Artifact",
        "source_stage": "06 Backtesting Engine",
        "diagnostics_id": "raw-stage06-001",
    }

    with pytest.raises(Stage08IntakeError, match="raw"):
        validate_stage07_risk_handoff_package(payload)


def test_stage08_rejects_raw_motor_inputs() -> None:
    payload = {
        "source_motor": "MotorB",
        "source_artifact_type": "MotorBRawDiagnosticsInputForStage07",
        "motor_b_input_id": "raw-motor-b-001",
    }

    with pytest.raises(Stage08IntakeError, match="raw"):
        validate_stage07_risk_handoff_package(payload)


def test_stage08_fails_closed_when_critical_fields_missing() -> None:
    payload = default_stage07_risk_handoff_payload()
    payload.pop("non_approval_statement")

    with pytest.raises(Stage08IntakeError, match="missing_critical_fields"):
        validate_stage07_risk_handoff_package(payload)
