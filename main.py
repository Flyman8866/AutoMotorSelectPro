from __future__ import annotations

from pathlib import Path
import sys
import argparse

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from automotorselectpro.constants import DEMO_DISCLAIMER
from automotorselectpro.motor_db import demo_motors
from automotorselectpro.motion import MotionProfile
from automotorselectpro.filtering import SelectionCriteria, filter_motors


def run_smoke_test() -> int:
    profile = MotionProfile(accel_rpm_per_s=4000, target_rpm=2500, load_inertia=0.0025, load_torque_nm=2.0)
    criteria = SelectionCriteria(
        required_peak_torque_nm=6.0,
        required_rms_torque_nm=2.5,
        required_speed_rpm=2500,
        max_inertia_ratio=12.0,
        axis_vertical=False,
        require_brake=False,
    )
    result = filter_motors(demo_motors(), profile, criteria)
    if not result.qualified:
        print("Smoke test failed: no qualified motors")
        return 1
    print("SMOKE_TEST_OK")
    print(DEMO_DISCLAIMER)
    print(f"Qualified count: {len(result.qualified)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="AutoMotorSelectPro")
    parser.add_argument("--smoke-test", action="store_true", help="run a non-GUI smoke test")
    args = parser.parse_args(argv)

    if args.smoke_test:
        return run_smoke_test()

    from automotorselectpro.gui import run_app

    return run_app()


if __name__ == "__main__":
    raise SystemExit(main())
