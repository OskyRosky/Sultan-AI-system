"""Pre-execution governance gate for 06B.

Block 07 is not a simulation engine. A passed gate means only that the adapted
package and the metadata-only temporal result may proceed to a future empirical
execution stage. It does not mean simulation executed, strategy validation,
profitability, OOS, walk-forward, robustness, or confidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from adapters.strategy_dossier_adapter import AdaptedBacktestPackage
from validators.temporal_admissibility_validator import (
    TemporalAdmissibilityResult,
    TemporalAdmissibilityStatus,
)


class GovernanceGateStatus(str, Enum):
    PASSED = "passed"
    REJECTED = "rejected"
    INSUFFICIENT_INFORMATION = "insufficient_information"


@dataclass(frozen=True)
class GovernanceGateResult:
    package_id: str
    strategy_id: str
    strategy_version: str
    snapshot_id: str
    gate_status: GovernanceGateStatus
    gate_reason: str
    certification_scope: str
    validation_timestamp: datetime
    blocking_failures: tuple[str, ...]
    warnings: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.gate_status, GovernanceGateStatus):
            raise TypeError("gate_status must be a GovernanceGateStatus")

    def to_dict(self) -> dict[str, Any]:
        return {
            "package_id": self.package_id,
            "strategy_id": self.strategy_id,
            "strategy_version": self.strategy_version,
            "snapshot_id": self.snapshot_id,
            "gate_status": self.gate_status.value,
            "gate_reason": self.gate_reason,
            "certification_scope": self.certification_scope,
            "validation_timestamp": self.validation_timestamp.isoformat(),
            "blocking_failures": list(self.blocking_failures),
            "warnings": list(self.warnings),
        }


class PreExecutionGovernanceGate:
    """Validate pre-execution governance handoff without empirical execution."""

    def __init__(
        self,
        adapted_package: AdaptedBacktestPackage,
        temporal_result: TemporalAdmissibilityResult,
        *,
        validation_timestamp: datetime | None = None,
    ) -> None:
        self.adapted_package = adapted_package
        self.temporal_result = temporal_result
        self.validation_timestamp = validation_timestamp or datetime(
            1970,
            1,
            1,
            tzinfo=timezone.utc,
        )

    def evaluate(self) -> GovernanceGateResult:
        package = self.adapted_package
        temporal = self.temporal_result
        missing: list[str] = []
        failures: list[str] = []
        warnings = [
            "PASSED means only that the package may proceed to a future empirical "
            "execution stage; it does not mean simulation executed, strategy "
            "validated, strategy profitable, OOS passed, walk-forward passed, "
            "robustness passed, or confidence established."
        ]

        _require_text(package.adapted_package_id, "package_id", missing)
        _require_text(package.strategy_id, "strategy_id", missing)
        _require_text(package.strategy_version, "strategy_version", missing)
        _require_text(package.snapshot_id, "snapshot_id", missing)
        _require_text(package.feature_version, "feature_version", missing)
        _require_text(package.code_commit, "code_commit", missing)
        _require_path(package.manifest_path, "manifest_path", missing)
        _require_path(package.schema_path, "schema_path", missing)
        _require_text(package.gap_report_reference, "gap_report_reference", missing)
        _require_text(
            package.quality_report_reference,
            "quality_report_reference",
            missing,
        )

        _validate_temporal_result(package, temporal, missing, failures)
        _validate_governance_state(package, failures)
        _validate_series(package, missing, failures)

        if missing:
            missing_status = (
                GovernanceGateStatus.INSUFFICIENT_INFORMATION
                if any(failure.startswith("temporal ") for failure in missing)
                else GovernanceGateStatus.REJECTED
            )
            return _result(
                package,
                temporal,
                self.validation_timestamp,
                missing_status,
                "Pre-execution governance gate cannot pass because required metadata is missing.",
                tuple(dict.fromkeys(missing)),
                tuple(warnings),
            )

        if failures:
            return _result(
                package,
                temporal,
                self.validation_timestamp,
                GovernanceGateStatus.REJECTED,
                "Pre-execution governance gate rejected the package due to blocking governance failures.",
                tuple(dict.fromkeys(failures)),
                tuple(warnings),
            )

        return _result(
            package,
            temporal,
            self.validation_timestamp,
            GovernanceGateStatus.PASSED,
            "Package may proceed to a future empirical execution stage. This does not "
            "mean simulation executed, strategy validated, strategy profitable, OOS "
            "passed, walk-forward passed, robustness passed, or confidence established.",
            (),
            tuple(warnings),
        )


def evaluate_pre_execution_governance(
    adapted_package: AdaptedBacktestPackage,
    temporal_result: TemporalAdmissibilityResult,
    *,
    validation_timestamp: datetime | None = None,
) -> GovernanceGateResult:
    return PreExecutionGovernanceGate(
        adapted_package,
        temporal_result,
        validation_timestamp=validation_timestamp,
    ).evaluate()


def _validate_temporal_result(
    package: AdaptedBacktestPackage,
    temporal: TemporalAdmissibilityResult,
    missing: list[str],
    failures: list[str],
) -> None:
    _require_text(temporal.package_id, "temporal.package_id", missing)
    _require_text(temporal.strategy_id, "temporal.strategy_id", missing)
    _require_text(temporal.strategy_version, "temporal.strategy_version", missing)
    _require_text(temporal.snapshot_id, "temporal.snapshot_id", missing)

    if temporal.package_id != package.adapted_package_id:
        failures.append("temporal package_id must match adapted package")
    if temporal.strategy_id != package.strategy_id:
        failures.append("temporal strategy_id must match adapted package")
    if temporal.strategy_version != package.strategy_version:
        failures.append("temporal strategy_version must match adapted package")
    if temporal.snapshot_id != package.snapshot_id:
        failures.append("temporal snapshot_id must match adapted package")

    if temporal.certification_scope != "package_metadata_only":
        failures.append("certification_scope must be package_metadata_only")
    if temporal.handoff_required is not True:
        failures.append("handoff_required must be true")
    if temporal.handoff_target != "Block 07":
        failures.append("handoff_target must be Block 07")
    if temporal.certification_status is TemporalAdmissibilityStatus.REJECTED:
        failures.append("temporal certification is rejected")
    elif (
        temporal.certification_status
        is TemporalAdmissibilityStatus.INSUFFICIENT_INFORMATION
    ):
        missing.append("temporal certification has insufficient information")
    elif temporal.certification_status is not TemporalAdmissibilityStatus.CERTIFIED:
        failures.append("temporal certification status is not certified")
    if temporal.admissible is not True:
        if (
            temporal.certification_status
            is TemporalAdmissibilityStatus.INSUFFICIENT_INFORMATION
        ):
            missing.append("temporal admissible must be true")
        else:
            failures.append("temporal admissible must be true")


def _validate_governance_state(
    package: AdaptedBacktestPackage,
    failures: list[str],
) -> None:
    governance = package.governance_state
    if governance.stage_09_readiness != "blocked":
        failures.append("Stage 09 readiness must remain blocked")
    if governance.handoff_to_09 != "blocked":
        failures.append("handoff_to_09 must remain blocked")
    if governance.paper_trading_eligibility != "blocked":
        failures.append("paper trading eligibility must remain blocked")
    if governance.temporal_admissibility_status != "temporal_admissibility_not_certified":
        failures.append("governance temporal admissibility status must remain not certified")
    if governance.simulation_status != "backtest_not_implemented":
        failures.append("simulation status must remain backtest_not_implemented")
    if governance.empirical_results_available is not False:
        failures.append("empirical results must not be available")


def _validate_series(
    package: AdaptedBacktestPackage,
    missing: list[str],
    failures: list[str],
) -> None:
    if not package.series:
        missing.append("series must contain at least one item")
        return

    seen_series: set[tuple[str, str]] = set()
    for key, series in package.series.items():
        series_key = (series.symbol, series.timeframe)
        if key != series_key:
            failures.append(f"series key {key} does not match metadata key {series_key}")
        if series_key in seen_series:
            failures.append(f"duplicate symbol/timeframe series: {series_key}")
        seen_series.add(series_key)

        _require_text(series.symbol, "series.symbol", missing)
        _require_text(series.timeframe, "series.timeframe", missing)
        if series.row_count <= 0:
            failures.append(
                f"series {series.symbol}/{series.timeframe} row_count must be positive"
            )
        if series.min_timestamp is None:
            missing.append(f"series {series.symbol}/{series.timeframe} min_timestamp missing")
        if series.max_timestamp is None:
            missing.append(f"series {series.symbol}/{series.timeframe} max_timestamp missing")
        if series.min_timestamp is not None and series.max_timestamp is not None:
            if series.min_timestamp > series.max_timestamp:
                failures.append(
                    f"series {series.symbol}/{series.timeframe} min_timestamp "
                    "must be <= max_timestamp"
                )


def _result(
    package: AdaptedBacktestPackage,
    temporal: TemporalAdmissibilityResult,
    validation_timestamp: datetime,
    status: GovernanceGateStatus,
    reason: str,
    blocking_failures: tuple[str, ...],
    warnings: tuple[str, ...],
) -> GovernanceGateResult:
    return GovernanceGateResult(
        package_id=package.adapted_package_id,
        strategy_id=package.strategy_id,
        strategy_version=package.strategy_version,
        snapshot_id=package.snapshot_id,
        gate_status=status,
        gate_reason=reason,
        certification_scope=temporal.certification_scope,
        validation_timestamp=validation_timestamp,
        blocking_failures=blocking_failures,
        warnings=warnings,
    )


def _require_text(value: object, field_name: str, missing: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        missing.append(f"{field_name} must be present")


def _require_path(value: object, field_name: str, missing: list[str]) -> None:
    if not isinstance(value, Path) or not str(value).strip() or not value.is_file():
        missing.append(f"{field_name} must reference an existing file")
