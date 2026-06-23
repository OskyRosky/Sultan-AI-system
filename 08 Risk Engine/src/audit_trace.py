from __future__ import annotations

import hashlib
import json
from typing import Any

from contracts import DRY_RUN_TIMESTAMP, NON_APPROVAL_STATEMENT, STAGE08_ID, Stage08AuditTrace


def stable_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


def stable_hash(prefix: str, payload: Any) -> str:
    digest = hashlib.sha256(stable_json(payload).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


def create_audit_trace(
    input_package: Any,
    gate_results: tuple[Any, ...],
    risk_decision: Any,
) -> Stage08AuditTrace:
    input_dict = input_package.to_dict()
    gate_dicts = tuple(gate.to_dict() for gate in gate_results)
    decision_dict = risk_decision.to_dict()
    artifact_hashes = (
        stable_hash("stage08-input", input_dict),
        *(stable_hash("stage08-gate", gate) for gate in gate_dicts),
        stable_hash("stage08-decision", decision_dict),
    )
    blocking_gaps = tuple(
        sorted(
            set(input_dict.get("blocking_gaps", ()))
            | {
                gap
                for gate in gate_dicts
                for gap in gate.get("blocking_gaps", ())
            }
            | set(decision_dict.get("blocking_gaps", ()))
        )
    )
    forbidden = tuple(sorted(decision_dict.get("forbidden_downstream_usage", ())))
    payload = {
        "stage_id": STAGE08_ID,
        "source_risk_handoff_package_id": input_dict["source_risk_handoff_package_id"],
        "artifact_hashes": artifact_hashes,
        "gate_names": tuple(gate["gate_name"] for gate in gate_dicts),
        "decision_hash": stable_hash("stage08-decision", decision_dict),
        "blocking_gaps": blocking_gaps,
    }
    return Stage08AuditTrace(
        audit_trace_id=stable_hash("stage08-audit", payload),
        stage_id=STAGE08_ID,
        dry_run_timestamp=DRY_RUN_TIMESTAMP,
        source_artifacts=("RiskHandoffPackage",),
        artifact_hashes=artifact_hashes,
        gate_names=tuple(gate["gate_name"] for gate in gate_dicts),
        decision_hash=stable_hash("stage08-decision", decision_dict),
        blocking_gaps=blocking_gaps,
        forbidden_downstream_usage=forbidden,
        non_approval_statement=NON_APPROVAL_STATEMENT,
    )
