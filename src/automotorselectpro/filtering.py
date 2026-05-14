from __future__ import annotations

from dataclasses import dataclass, field

from .motor_db import Motor
from .motion import MotionProfile


@dataclass(slots=True)
class SelectionCriteria:
    required_peak_torque_nm: float
    required_rms_torque_nm: float
    required_speed_rpm: int
    max_inertia_ratio: float
    axis_vertical: bool
    require_brake: bool


@dataclass(slots=True)
class Evaluation:
    motor: Motor
    reasons: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.reasons


@dataclass(slots=True)
class FilterResult:
    qualified: list[Motor]
    rejected: list[Evaluation]


def _inertia_ratio(load_inertia: float, rotor_inertia: float) -> float:
    if rotor_inertia <= 0:
        return float("inf")
    return load_inertia / rotor_inertia


def evaluate_motor(motor: Motor, profile: MotionProfile, criteria: SelectionCriteria) -> Evaluation:
    reasons: list[str] = []

    if motor.peak_torque_nm < criteria.required_peak_torque_nm:
        reasons.append("REJECT_PEAK_TORQUE_INSUFFICIENT")

    if motor.rms_torque_nm < criteria.required_rms_torque_nm:
        reasons.append("REJECT_RMS_TORQUE_INSUFFICIENT")

    if motor.max_speed_rpm < criteria.required_speed_rpm:
        reasons.append("REJECT_MAX_SPEED_INSUFFICIENT")

    ratio = _inertia_ratio(profile.load_inertia, motor.rotor_inertia)
    if ratio > criteria.max_inertia_ratio:
        reasons.append("REJECT_INERTIA_RATIO_TOO_HIGH")

    if criteria.axis_vertical and criteria.require_brake and not motor.has_brake:
        reasons.append("REJECT_VERTICAL_AXIS_BRAKE_REQUIRED")

    return Evaluation(motor=motor, reasons=reasons)


def filter_motors(motors: list[Motor], profile: MotionProfile, criteria: SelectionCriteria) -> FilterResult:
    qualified: list[Motor] = []
    rejected: list[Evaluation] = []

    for motor in motors:
        evaluation = evaluate_motor(motor, profile, criteria)
        if evaluation.passed:
            qualified.append(motor)
        else:
            rejected.append(evaluation)

    return FilterResult(qualified=qualified, rejected=rejected)
