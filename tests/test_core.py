from automotorselectpro.constants import DEMO_DISCLAIMER
from automotorselectpro.filtering import SelectionCriteria, evaluate_motor, filter_motors
from automotorselectpro.motion import MotionProfile
from automotorselectpro.motor_db import Motor, demo_motors


def test_demo_disclaimer_flag():
    assert DEMO_DISCLAIMER == "DEMO_ONLY_NOT_FOR_ENGINEERING_USE"


def test_hard_filter_peak_rms_speed():
    motor = Motor("X", peak_torque_nm=3.0, rms_torque_nm=1.0, max_speed_rpm=1000, rotor_inertia=0.001, has_brake=False)
    profile = MotionProfile(accel_rpm_per_s=2000, target_rpm=1500, load_inertia=0.001, load_torque_nm=1.0)
    criteria = SelectionCriteria(5.0, 2.0, 1500, 10.0, False, False)
    eva = evaluate_motor(motor, profile, criteria)
    assert "REJECT_PEAK_TORQUE_INSUFFICIENT" in eva.reasons
    assert "REJECT_RMS_TORQUE_INSUFFICIENT" in eva.reasons
    assert "REJECT_MAX_SPEED_INSUFFICIENT" in eva.reasons


def test_inertia_ratio_reject():
    motor = Motor("X", peak_torque_nm=10.0, rms_torque_nm=4.0, max_speed_rpm=3000, rotor_inertia=0.0001, has_brake=True)
    profile = MotionProfile(accel_rpm_per_s=2000, target_rpm=1500, load_inertia=0.01, load_torque_nm=1.0)
    criteria = SelectionCriteria(5.0, 2.0, 1500, 20.0, False, False)
    eva = evaluate_motor(motor, profile, criteria)
    assert "REJECT_INERTIA_RATIO_TOO_HIGH" in eva.reasons


def test_vertical_axis_brake_required():
    motor = Motor("X", peak_torque_nm=10.0, rms_torque_nm=4.0, max_speed_rpm=3000, rotor_inertia=0.001, has_brake=False)
    profile = MotionProfile(accel_rpm_per_s=1000, target_rpm=1000, load_inertia=0.001, load_torque_nm=0.5)
    criteria = SelectionCriteria(3.0, 1.0, 1000, 10.0, True, True)
    eva = evaluate_motor(motor, profile, criteria)
    assert "REJECT_VERTICAL_AXIS_BRAKE_REQUIRED" in eva.reasons


def test_filter_has_qualified_demo_motor():
    profile = MotionProfile(accel_rpm_per_s=3000, target_rpm=2500, load_inertia=0.002, load_torque_nm=2.0)
    criteria = SelectionCriteria(6.0, 2.0, 2500, 10.0, False, False)
    result = filter_motors(demo_motors(), profile, criteria)
    assert len(result.qualified) >= 1
