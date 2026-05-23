"""Fictitious mockups for the Strategy Inputs Contract.

These records are synthetic governance examples only. They are not real
research evidence, do not represent edge, and must not be interpreted as
signals, rules, strategy candidates, or trading approval.
"""

from __future__ import annotations

from datetime import datetime, timezone

from strategy.inputs_contract import (
    FindingInput,
    HypothesisInput,
    ResearchEvidenceInput,
    SourceStatus,
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
    source_status="closed",
    created_at=MOCK_CREATED_AT,
    limitations=("Synthetic evidence mockup; not real market evidence.",),
    audit_reference="mock-audit-evidence-001",
)


FICTITIOUS_FINDING_UNADMISSIBLE_STATUS = FindingInput(
    finding_id="mock-finding-unadmissible-status",
    linked_evidence_ids=("mock-evidence-001",),
    finding_summary="Fictitious finding with source status under review.",
    finding_type="synthetic_example",
    regime_scope="mock_regime_context",
    stability_assessment="synthetic_stability_assessment",
    informativeness_assessment="synthetic_informativeness_assessment",
    falsification_reference=None,
    source_status=SourceStatus.UNDER_REVIEW,
    closure_reference="mock-closure-reference",
    audit_reference="mock-audit-finding-unadmissible-status",
    limitations=("Synthetic finding; not real research.",),
)


FICTITIOUS_FINDING_INCOMPLETE_TRACEABILITY = FindingInput(
    finding_id="mock-finding-incomplete-traceability",
    linked_evidence_ids=(),
    finding_summary="Fictitious finding without linked evidence.",
    finding_type="synthetic_example",
    regime_scope="mock_regime_context",
    stability_assessment="synthetic_stability_assessment",
    informativeness_assessment="synthetic_informativeness_assessment",
    falsification_reference=None,
    source_status=SourceStatus.PROMOTED_TO_QUALITY_REVIEW,
    closure_reference="mock-closure-reference",
    audit_reference="mock-audit-finding-incomplete-traceability",
    limitations=("Synthetic finding; not real research.",),
)


FICTITIOUS_FINDING_MISSING_LIMITATIONS = FindingInput(
    finding_id="mock-finding-missing-limitations",
    linked_evidence_ids=("mock-evidence-001",),
    finding_summary="Fictitious finding without limitations.",
    finding_type="synthetic_example",
    regime_scope="mock_regime_context",
    stability_assessment="synthetic_stability_assessment",
    informativeness_assessment="synthetic_informativeness_assessment",
    falsification_reference=None,
    source_status=SourceStatus.PROMOTED_TO_QUALITY_REVIEW,
    closure_reference="mock-closure-reference",
    audit_reference="mock-audit-finding-missing-limitations",
    limitations=(),
)


FICTITIOUS_FINDING_ELIGIBLE = FindingInput(
    finding_id="mock-finding-eligible",
    linked_evidence_ids=("mock-evidence-001",),
    finding_summary="Fictitious finding eligible for conceptual design only.",
    finding_type="synthetic_example",
    regime_scope="mock_regime_context",
    stability_assessment="synthetic_stability_assessment",
    informativeness_assessment="synthetic_informativeness_assessment",
    falsification_reference=None,
    source_status=SourceStatus.PROMOTED_TO_QUALITY_REVIEW,
    closure_reference="mock-closure-reference",
    audit_reference="mock-audit-finding-eligible",
    limitations=("Synthetic finding; not real research or edge.",),
)


FICTITIOUS_HYPOTHESIS_NONADMISSIBLE_STATUS = HypothesisInput(
    hypothesis_id="mock-hypothesis-nonadmissible-status",
    linked_finding_ids=("mock-finding-001",),
    linked_evidence_ids=("mock-evidence-001",),
    hypothesis_statement="Fictitious hypothesis for contract rejection testing.",
    expected_behavior="No real expected behavior; synthetic example only.",
    applicable_regime_context="mock_regime_context",
    falsification_criteria=("Synthetic falsification criterion.",),
    limitations=("Synthetic hypothesis; not real research.",),
    source_status=SourceStatus.PROPOSED,
    audit_reference="mock-audit-hypothesis-nonadmissible-status",
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
    source_status=SourceStatus.PROMOTED_FOR_STRATEGY_REVIEW,
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
    source_status=SourceStatus.PROMOTED_FOR_STRATEGY_REVIEW,
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
    source_status=SourceStatus.PROMOTED_FOR_STRATEGY_REVIEW,
    audit_reference="mock-audit-hypothesis-eligible",
)
