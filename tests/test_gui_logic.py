import pytest

from automotorselectpro.constants import DEMO_DISCLAIMER
from automotorselectpro.gui_logic import UserInputs, build_selection_criteria, run_selection
from automotorselectpro.motor_db import demo_motors


def _base_inputs() -> UserInputs:
    return UserInputs(
        axis_name="Axis-1",
        axis_type="水平轴",
        required_peak_torque_nm="6.0",
        required_rms_torque_nm="2.0",
        required_speed_rpm="2500",
        load_inertia="0.002",
        max_inertia_ratio="10.0",
        axis_vertical=False,
        require_brake=False,
    )


def test_invalid_max_inertia_ratio():
    inputs = _base_inputs()
    inputs.max_inertia_ratio = "0.5"
    with pytest.raises(ValueError):
        build_selection_criteria(inputs)


def test_vertical_axis_warning_when_no_brake():
    inputs = _base_inputs()
    inputs.axis_vertical = True
    inputs.require_brake = False
    _, _, warnings = build_selection_criteria(inputs)
    assert warnings


def test_selection_has_qualified_and_rejected_reasons():
    result, _ = run_selection(_base_inputs(), demo_motors())
    assert result.qualified
    assert any(e.reasons for e in result.rejected)


def test_demo_disclaimer_still_set():
    assert DEMO_DISCLAIMER == "DEMO_ONLY_NOT_FOR_ENGINEERING_USE"
