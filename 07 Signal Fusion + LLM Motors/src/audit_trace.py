from __future__ import annotations

import hashlib
import json
from typing import Any

from contracts import (
    DRY_RUN_TIMESTAMP,
    FORBIDDEN_DOWNSTREAM_USAGE,
    NON_APPROVAL_STATEMENT,
    Stage07AuditTrace,
)


def stable_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)


def stable_hash(prefix: str, payload: Any) -> str:
    digest = hashlib.sha256(stable_json(payload).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


def create_audit_trace(artifacts: tuple[Any, ...]) -> Stage07AuditTrace:
    artifact_dicts = tuple(
        artifact.to_dict() if hasattr(artifact, "to_dict") else artifact
        for artifact in artifacts
    )
    artifact_hashes = tuple(stable_hash("artifact", item) for item in artifact_dicts)
    blocking_gaps = tuple(
        sorted(
            {
                gap
                for item in artifact_dicts
                for gap in item.get("blocking_gaps", ())
            }
        )
    )
    source_artifacts = tuple(
        item.get("source_artifact_type", item.get("source_motor", item.get("target_stage", "stage07_artifact")))
        for item in artifact_dicts
    )
    payload = {
        "stage_id": "07 Signal Fusion + LLM Motors",
        "dry_run_timestamp": DRY_RUN_TIMESTAMP,
        "artifact_hashes": artifact_hashes,
        "blocking_gaps": blocking_gaps,
    }
    return Stage07AuditTrace(
        audit_trace_id=stable_hash("stage07-audit", payload),
        stage_id="07 Signal Fusion + LLM Motors",
        dry_run_timestamp=DRY_RUN_TIMESTAMP,
        source_artifacts=source_artifacts,
        artifact_hashes=artifact_hashes,
        blocking_gaps=blocking_gaps,
        forbidden_downstream_usage=FORBIDDEN_DOWNSTREAM_USAGE,
        non_approval_statement=NON_APPROVAL_STATEMENT,
    )
