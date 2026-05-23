"""Fictitious mockups for the Strategy Inputs Contract.

These records are synthetic governance examples only. They are not real
research evidence, do not represent edge, and must not be interpreted as
signals, rules, strategy candidates, or trading approval.
"""

from __future__ import annotations

from datetime import datetime, timezone

from strategy.inputs_contract import (
    ApprovalStatus,
    HypothesisInput,
    ResearchEvidenceInput,
)


MOCK_CREATED_AT = datetime(2026, 1, 1, tzinfo=timezone.utc)


FICTITIOUS_EVIDENCE_INELIGIBLE = ResearchEvidenceInput(
    evidence_id="mock-evidence-001",
    source_layer="04 Research Layer",
    source_component="mock_feature_informativeness",
    evidence_type="synthetic_example",
    feature_reference="mock_feature_only",
    target_reference="mock_forward_return_1h",
    regime_reference="mock_regime_context",
    temporal_scope="synthetic_time_window",
    asset_scope="synthetic_asset_scope",
    timeframe_scope="synthetic_timeframe",
    evidence_status="closed",
    approval_status=ApprovalStatus.APPROVED,
    created_at=MOCK_CREATED_AT,
    limitations=("Synthetic evidence mockup; not real market evidence.",),
    audit_reference="mock-audit-evidence-001",
)


FICTITIOUS_HYPOTHESIS_UNAPPROVED = HypothesisInput(
    hypothesis_id="mock-hypothesis-unapproved",
    linked_finding_ids=("mock-finding-001",),
    linked_evidence_ids=("mock-evidence-001",),
    hypothesis_statement="Fictitious hypothesis for contract rejection testing.",
    expected_behavior="No real expected behavior; synthetic example only.",
    applicable_regime_context="mock_regime_context",
    falsification_criteria=("Synthetic falsification criterion.",),
    limitations=("Synthetic hypothesis; not real research.",),
    approval_status=ApprovalStatus.PENDING_REVIEW,
    eligible_for_strategy_design=False,
    audit_reference="mock-audit-hypothesis-unapproved",
)


FICTITIOUS_HYPOTHESIS_MISSING_FALSIFICATION = HypothesisInput(
    hypothesis_id="mock-hypothesis-missing-falsification",
    linked_finding_ids=("mock-finding-001",),
    linked_evidence_ids=("mock-evidence-001",),
    hypothesis_statement="Fictitious hypothesis with missing falsification criteria.",
    expected_behavior="No real expected behavior; synthetic example only.",
    applicable_regime_context="mock_regime_context",
    falsification_criteria=(),
    limitations=("Synthetic hypothesis; not real research.",),
    approval_status=ApprovalStatus.APPROVED,
    eligible_for_strategy_design=True,
    audit_reference="mock-audit-hypothesis-missing-falsification",
)


FICTITIOUS_HYPOTHESIS_INCOMPLETE_TRACEABILITY = HypothesisInput(
    hypothesis_id="mock-hypothesis-incomplete-traceability",
    linked_finding_ids=("mock-finding-001",),
    linked_evidence_ids=(),
    hypothesis_statement="Fictitious hypothesis with incomplete traceability.",
    expected_behavior="No real expected behavior; synthetic example only.",
    applicable_regime_context="mock_regime_context",
    falsification_criteria=("Synthetic falsification criterion.",),
    limitations=("Synthetic hypothesis; not real research.",),
    approval_status=ApprovalStatus.APPROVED,
    eligible_for_strategy_design=True,
    audit_reference="mock-audit-hypothesis-incomplete-traceability",
)


FICTITIOUS_HYPOTHESIS_ELIGIBLE = HypothesisInput(
    hypothesis_id="mock-hypothesis-eligible",
    linked_finding_ids=("mock-finding-001",),
    linked_evidence_ids=("mock-evidence-001",),
    hypothesis_statement="Fictitious hypothesis eligible for conceptual design only.",
    expected_behavior="No real expected behavior; synthetic example only.",
    applicable_regime_context="mock_regime_context",
    falsification_criteria=("Synthetic rejection criterion exists.",),
    limitations=("Synthetic hypothesis; not real research or edge.",),
    approval_status=ApprovalStatus.APPROVED,
    eligible_for_strategy_design=True,
    audit_reference="mock-audit-hypothesis-eligible",
)
