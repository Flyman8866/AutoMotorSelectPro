from __future__ import annotations

from dataclasses import dataclass

from .filtering import FilterResult, SelectionCriteria, filter_motors
from .motion import MotionProfile
from .motor_db import Motor


@dataclass(slots=True)
class UserInputs:
    axis_name: str
    axis_type: str
    required_peak_torque_nm: str
    required_rms_torque_nm: str
    required_speed_rpm: str
    load_inertia: str
    max_inertia_ratio: str
    axis_vertical: bool
    require_brake: bool


def _parse_positive(name: str, value: str) -> float:
    if value is None or str(value).strip() == "":
        raise ValueError(f"{name} 不能为空")
    try:
        num = float(value)
    except ValueError as exc:
        raise ValueError(f"{name} 必须是数字") from exc
    if num <= 0:
        raise ValueError(f"{name} 必须大于 0")
    return num


def build_selection_criteria(inputs: UserInputs) -> tuple[SelectionCriteria, MotionProfile, list[str]]:
    if not inputs.axis_name.strip():
        raise ValueError("轴名称不能为空")

    required_peak = _parse_positive("所需峰值转矩", inputs.required_peak_torque_nm)
    required_rms = _parse_positive("所需RMS转矩", inputs.required_rms_torque_nm)
    required_speed = int(_parse_positive("所需最高转速", inputs.required_speed_rpm))
    load_inertia = _parse_positive("折算负载惯量", inputs.load_inertia)
    max_inertia_ratio = _parse_positive("最大允许惯量比", inputs.max_inertia_ratio)

    if max_inertia_ratio < 1:
        raise ValueError("最大允许惯量比不能小于 1")

    warnings: list[str] = []
    if inputs.axis_vertical and not inputs.require_brake:
        warnings.append("安全提醒：垂直轴通常需要抱闸，请确认机械安全设计。")

    criteria = SelectionCriteria(
        required_peak_torque_nm=required_peak,
        required_rms_torque_nm=required_rms,
        required_speed_rpm=required_speed,
        max_inertia_ratio=max_inertia_ratio,
        axis_vertical=inputs.axis_vertical,
        require_brake=inputs.require_brake,
    )
    profile = MotionProfile(
        accel_rpm_per_s=1.0,
        target_rpm=required_speed,
        load_inertia=load_inertia,
        load_torque_nm=0.0,
    )
    return criteria, profile, warnings


def run_selection(inputs: UserInputs, motors: list[Motor]) -> tuple[FilterResult, list[str]]:
    criteria, profile, warnings = build_selection_criteria(inputs)
    return filter_motors(motors, profile, criteria), warnings
