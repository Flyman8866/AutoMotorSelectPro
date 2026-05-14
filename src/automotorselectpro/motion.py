from __future__ import annotations

from dataclasses import dataclass

from .units import rpm_to_rad_s


@dataclass(slots=True)
class MotionProfile:
    accel_rpm_per_s: float
    target_rpm: float
    load_inertia: float
    load_torque_nm: float = 0.0

    def accel_rad_s2(self) -> float:
        return rpm_to_rad_s(self.accel_rpm_per_s)

    def required_accel_torque_nm(self) -> float:
        return self.load_inertia * self.accel_rad_s2()

    def required_peak_torque_nm(self) -> float:
        return self.required_accel_torque_nm() + self.load_torque_nm
