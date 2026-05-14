from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Motor:
    model: str
    peak_torque_nm: float
    rms_torque_nm: float
    max_speed_rpm: int
    rotor_inertia: float
    has_brake: bool


def demo_motors() -> list[Motor]:
    return [
        Motor("MSP-100A", 4.2, 1.5, 3000, 0.00025, False),
        Motor("MSP-200B", 8.5, 3.0, 3000, 0.00045, True),
        Motor("MSP-400C", 13.0, 5.5, 4500, 0.0012, True),
        Motor("MSP-750D", 22.0, 9.0, 3500, 0.0028, True),
        Motor("MSP-90N", 5.5, 2.2, 2000, 0.0002, False),
    ]
