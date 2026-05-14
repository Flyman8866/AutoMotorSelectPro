from __future__ import annotations

import sys

from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .constants import APP_NAME, APP_VERSION, DEMO_DISCLAIMER
from .filtering import SelectionCriteria, filter_motors
from .motion import MotionProfile
from .motor_db import demo_motors


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")

        self.label = QLabel(DEMO_DISCLAIMER)
        self.button = QPushButton("Run Demo Selection")
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Model", "Peak(Nm)", "RMS(Nm)", "Speed(rpm)"])

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.table)
        self.setCentralWidget(container)

        self.button.clicked.connect(self._run_selection)

    def _run_selection(self) -> None:
        profile = MotionProfile(accel_rpm_per_s=3000, target_rpm=2500, load_inertia=0.002, load_torque_nm=2.0)
        criteria = SelectionCriteria(6.0, 2.0, 2500, 10.0, axis_vertical=False, require_brake=False)
        result = filter_motors(demo_motors(), profile, criteria)

        self.table.setRowCount(len(result.qualified))
        for r, m in enumerate(result.qualified):
            self.table.setItem(r, 0, QTableWidgetItem(m.model))
            self.table.setItem(r, 1, QTableWidgetItem(f"{m.peak_torque_nm:.2f}"))
            self.table.setItem(r, 2, QTableWidgetItem(f"{m.rms_torque_nm:.2f}"))
            self.table.setItem(r, 3, QTableWidgetItem(str(m.max_speed_rpm)))


def run_app() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(720, 420)
    window.show()
    return app.exec()
