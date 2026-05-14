from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AxisConfig:
    name: str = "Axis"
    vertical: bool = False
    requires_brake: bool = False
