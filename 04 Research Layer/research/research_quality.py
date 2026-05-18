"""Pure in-memory research quality gates for Research Layer.

This module evaluates methodological quality of structured findings and
hypotheses. It does not approve trading, confirm alpha, create signals, or
promote strategies automatically.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import pandas as pd


QUALITY_STATUSES: tuple[str, ...] = ("pass", "warning", "fail", "insufficient_evidence")
VALID_FINDING_STATUSES: tuple[str, ...] = (
    "draft",
    "observed",
    "under_review",
    "rejected",
    "archived",
    "promoted_to_quality_review",
)
VALID_HYPOTHESIS_STATUSES: tuple[str, ...] = (
    "draft",
    "proposed",
    "rejected",
    "archived",
    "promoted_for_strategy_review",
)


@dataclass(frozen=True)
class QualityThresholds:
    """Explicit thresholds for research quality diagnostics."""

    minimum_sample_count: int = 30
    weak_ic_abs_threshold: float = 0.03
    max_nan_ratio: float = 0.20
    max_regime_concentration: float = 0.80
    max_period_concentration: float = 0.80
    minimum_regime_sample_count: int = 10


@dataclass(frozen=True)
class QualityReviewResult:
    """Structured in-memory output for one quality review."""

    subject_id: str
    subject_type: str
    quality_status: str
    passed_checks: tuple[str, ...]
    failed_checks: tuple[str, ...]
    warnings: tuple[str, ...]
    reviewer_notes: str
    evaluated_at: pd.Timestamp


def evaluate_finding_quality(
    finding: Mapping[str, object],
    *,
    hypothesis: Mapping[str, object] | None = None,
    thresholds: QualityThresholds = QualityThresholds(),
    reviewer_notes: str = "",
    evaluated_at: object | None = None,
) -> QualityReviewResult:
    """Evaluate minimum research quality gates for one finding record."""

    passed: list[str] = []
    failed: list[str] = []
    warnings: list[str] = []

    finding_id = _required_text(finding, "finding_id", failed)
    _check_status(finding, "status", VALID_FINDING_STATUSES, failed, subject="finding")

    supporting_metrics = _mapping_field(finding, "supporting_metrics", failed)
    sample_scope = _mapping_field(finding, "sample_scope", failed)
    limitations = _list_field(finding, "limitations", failed)
    caveats = _list_field(finding, "caveats", failed)

    if sample_scope:
        passed.append("sample_scope_present")
    if limitations:
        passed.append("limitations_present")
    if caveats:
        passed.append("caveats_present")

    sample_count = _numeric_metric(supporting_metrics, "sample_count")
    if sample_count is None:
        warnings.append("missing_sample_count")
    elif sample_count < thresholds.minimum_sample_count:
        failed.append("insufficient_sample_count")
    else:
        passed.append("minimum_sample_count")

    ic_value = _first_numeric_metric(supporting_metrics, ("pearson_ic", "spearman_ic", "ic"))
    if ic_value is None:
        warnings.append("missing_ic_metric")
    elif abs(ic_value) < thresholds.weak_ic_abs_threshold:
        warnings.append("weak_ic")
    else:
        passed.append("ic_not_weak")

    nan_ratio = _numeric_metric(supporting_metrics, "nan_ratio")
    if nan_ratio is None:
        warnings.append("missing_nan_ratio")
    elif nan_ratio > thresholds.max_nan_ratio:
        warnings.append("excessive_nan_ratio")
    else:
        passed.append("nan_ratio_within_limit")

    regime_concentration = _numeric_metric(supporting_metrics, "regime_concentration")
    if regime_concentration is not None:
        if regime_concentration > thresholds.max_regime_concentration:
            warnings.append("regime_concentration")
        else:
            passed.append("regime_concentration_within_limit")

    period_concentration = _numeric_metric(supporting_metrics, "period_concentration")
    if period_concentration is not None:
        if period_concentration > thresholds.max_period_concentration:
            warnings.append("temporal_concentration")
        else:
            passed.append("period_concentration_within_limit")

    min_regime_sample_count = _numeric_metric(supporting_metrics, "min_regime_sample_count")
    if min_regime_sample_count is not None:
        if min_regime_sample_count < thresholds.minimum_regime_sample_count:
            warnings.append("sparse_regime_evidence")
        else:
            passed.append("regime_sample_count")

    temporal_stability = _string_metric(supporting_metrics, "temporal_stability")
    if temporal_stability in {"unstable", "degraded"}:
        warnings.append("temporal_instability")

    if _string_metric(supporting_metrics, "ic_type") == "pooled":
        warnings.append("pooled_only_ic")

    if _string_metric(supporting_metrics, "multiple_testing_control") in {"", "none", "missing"}:
        warnings.append("missing_multiple_testing_control")

    if hypothesis is not None:
        _evaluate_hypothesis_governance(hypothesis, failed, warnings, passed)

    status = _quality_status(failed, warnings)
    if "insufficient_sample_count" in failed:
        status = "insufficient_evidence"

    return QualityReviewResult(
        subject_id=finding_id,
        subject_type="finding",
        quality_status=status,
        passed_checks=tuple(passed),
        failed_checks=tuple(failed),
        warnings=tuple(warnings),
        reviewer_notes=reviewer_notes,
        evaluated_at=_timestamp_or_now(evaluated_at),
    )


def evaluate_hypothesis_quality(
    hypothesis: Mapping[str, object],
    *,
    thresholds: QualityThresholds = QualityThresholds(),
    reviewer_notes: str = "",
    evaluated_at: object | None = None,
) -> QualityReviewResult:
    """Evaluate governance quality gates for one hypothesis record."""

    del thresholds
    passed: list[str] = []
    failed: list[str] = []
    warnings: list[str] = []
    hypothesis_id = _required_text(hypothesis, "hypothesis_id", failed)

    _evaluate_hypothesis_governance(hypothesis, failed, warnings, passed)

    return QualityReviewResult(
        subject_id=hypothesis_id,
        subject_type="hypothesis",
        quality_status=_quality_status(failed, warnings),
        passed_checks=tuple(passed),
        failed_checks=tuple(failed),
        warnings=tuple(warnings),
        reviewer_notes=reviewer_notes,
        evaluated_at=_timestamp_or_now(evaluated_at),
    )


def results_to_frame(results: Sequence[QualityReviewResult]) -> pd.DataFrame:
    """Convert quality review results to a DataFrame."""

    return pd.DataFrame(
        {
            "subject_id": result.subject_id,
            "subject_type": result.subject_type,
            "quality_status": result.quality_status,
            "passed_checks": list(result.passed_checks),
            "failed_checks": list(result.failed_checks),
            "warnings": list(result.warnings),
            "reviewer_notes": result.reviewer_notes,
            "evaluated_at": result.evaluated_at,
        }
        for result in results
    )


def _evaluate_hypothesis_governance(
    hypothesis: Mapping[str, object],
    failed: list[str],
    warnings: list[str],
    passed: list[str],
) -> None:
    _check_status(hypothesis, "status", VALID_HYPOTHESIS_STATUSES, failed, subject="hypothesis")

    falsification_conditions = _list_field(hypothesis, "falsification_conditions", failed)
    if falsification_conditions:
        passed.append("falsification_conditions_present")

    assumptions = _list_field(hypothesis, "assumptions", failed)
    if assumptions:
        passed.append("assumptions_present")
    else:
        warnings.append("missing_assumptions")


def _quality_status(failed: Sequence[str], warnings: Sequence[str]) -> str:
    if failed:
        return "fail"
    if warnings:
        return "warning"
    return "pass"


def _required_text(record: Mapping[str, object], field: str, failed: list[str]) -> str:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        failed.append(f"missing_{field}")
        return ""
    return value.strip()


def _mapping_field(record: Mapping[str, object], field: str, failed: list[str]) -> Mapping[str, object]:
    value = record.get(field)
    if not isinstance(value, Mapping) or not value:
        failed.append(f"missing_{field}")
        return {}
    return value


def _list_field(record: Mapping[str, object], field: str, failed: list[str]) -> Sequence[object]:
    value = record.get(field)
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or not value:
        failed.append(f"missing_{field}")
        return ()
    non_empty = [item for item in value if isinstance(item, str) and item.strip()]
    if not non_empty:
        failed.append(f"missing_{field}")
        return ()
    return tuple(non_empty)


def _check_status(
    record: Mapping[str, object],
    field: str,
    valid_statuses: Sequence[str],
    failed: list[str],
    *,
    subject: str,
) -> None:
    status = record.get(field)
    if status not in valid_statuses:
        failed.append(f"invalid_{subject}_status")


def _numeric_metric(metrics: Mapping[str, object], key: str) -> float | None:
    if key not in metrics:
        return None
    try:
        value = float(metrics[key])
    except (TypeError, ValueError):
        return None
    if pd.isna(value):
        return None
    return value


def _first_numeric_metric(metrics: Mapping[str, object], keys: Sequence[str]) -> float | None:
    for key in keys:
        value = _numeric_metric(metrics, key)
        if value is not None:
            return value
    return None


def _string_metric(metrics: Mapping[str, object], key: str) -> str:
    value = metrics.get(key, "")
    if value is None:
        return ""
    return str(value).strip().lower()


def _timestamp_or_now(value: object | None) -> pd.Timestamp:
    if value is None:
        return pd.Timestamp.now(tz="UTC")
    timestamp = pd.Timestamp(value)
    if pd.isna(timestamp):
        raise ValueError("evaluated_at must be a valid timestamp")
    return timestamp
