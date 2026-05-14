from __future__ import annotations

import sys

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .constants import APP_NAME, APP_VERSION, DEMO_DISCLAIMER
from .gui_logic import UserInputs, run_selection
from .motor_db import demo_motors


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} {APP_VERSION}")

        root = QWidget()
        root_layout = QHBoxLayout(root)

        left = QWidget()
        form = QFormLayout(left)

        self.axis_name_input = QLineEdit("Axis-1")
        self.axis_type_combo = QComboBox()
        self.axis_type_combo.addItems(["水平轴", "垂直轴", "转盘轴", "输送轴"])
        self.peak_input = QLineEdit("6.0")
        self.rms_input = QLineEdit("2.0")
        self.speed_input = QLineEdit("2500")
        self.load_inertia_input = QLineEdit("0.002")
        self.max_inertia_ratio_input = QLineEdit("10.0")
        self.axis_vertical_check = QCheckBox()
        self.require_brake_check = QCheckBox()

        form.addRow("轴名称", self.axis_name_input)
        form.addRow("轴类型", self.axis_type_combo)
        form.addRow("所需峰值转矩(Nm)", self.peak_input)
        form.addRow("所需RMS转矩(Nm)", self.rms_input)
        form.addRow("所需最高转速(rpm)", self.speed_input)
        form.addRow("折算负载惯量", self.load_inertia_input)
        form.addRow("最大允许惯量比", self.max_inertia_ratio_input)
        form.addRow("是否垂直轴", self.axis_vertical_check)
        form.addRow("是否需要抱闸", self.require_brake_check)

        self.run_button = QPushButton("计算并筛选电机")
        self.disclaimer = QLabel(DEMO_DISCLAIMER)
        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: orange;")
        form.addRow(self.run_button)
        form.addRow(self.disclaimer)
        form.addRow(self.warning_label)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.addWidget(QLabel("合格电机列表"))
        self.qualified_table = QTableWidget(0, 7)
        self.qualified_table.setHorizontalHeaderLabels([
            "Model", "Peak Torque Nm", "RMS Torque Nm", "Max Speed rpm", "Rotor Inertia", "Has Brake", "Data Source"
        ])
        right_layout.addWidget(self.qualified_table)

        right_layout.addWidget(QLabel("淘汰电机列表"))
        self.rejected_table = QTableWidget(0, 2)
        self.rejected_table.setHorizontalHeaderLabels(["Model", "Rejection Reasons"])
        right_layout.addWidget(self.rejected_table)

        root_layout.addWidget(left, 1)
        root_layout.addWidget(right, 2)
        self.setCentralWidget(root)

        self.axis_type_combo.currentTextChanged.connect(self._sync_axis_type)
        self.run_button.clicked.connect(self._run_selection)

    def _sync_axis_type(self) -> None:
        self.axis_vertical_check.setChecked(self.axis_type_combo.currentText() == "垂直轴")

    def _gather_inputs(self) -> UserInputs:
        return UserInputs(
            axis_name=self.axis_name_input.text(),
            axis_type=self.axis_type_combo.currentText(),
            required_peak_torque_nm=self.peak_input.text(),
            required_rms_torque_nm=self.rms_input.text(),
            required_speed_rpm=self.speed_input.text(),
            load_inertia=self.load_inertia_input.text(),
            max_inertia_ratio=self.max_inertia_ratio_input.text(),
            axis_vertical=self.axis_vertical_check.isChecked(),
            require_brake=self.require_brake_check.isChecked(),
        )

    def _run_selection(self) -> None:
        try:
            result, warnings = run_selection(self._gather_inputs(), demo_motors())
        except ValueError as exc:
            QMessageBox.warning(self, "输入错误", str(exc))
            return

        self.warning_label.setText("；".join(warnings))

        self.qualified_table.setRowCount(len(result.qualified))
        for r, m in enumerate(result.qualified):
            self.qualified_table.setItem(r, 0, QTableWidgetItem(m.model))
            self.qualified_table.setItem(r, 1, QTableWidgetItem(f"{m.peak_torque_nm:.2f}"))
            self.qualified_table.setItem(r, 2, QTableWidgetItem(f"{m.rms_torque_nm:.2f}"))
            self.qualified_table.setItem(r, 3, QTableWidgetItem(str(m.max_speed_rpm)))
            self.qualified_table.setItem(r, 4, QTableWidgetItem(f"{m.rotor_inertia:.6f}"))
            self.qualified_table.setItem(r, 5, QTableWidgetItem("Yes" if m.has_brake else "No"))
            self.qualified_table.setItem(r, 6, QTableWidgetItem("DEMO_DB"))

        self.rejected_table.setRowCount(len(result.rejected))
        for r, item in enumerate(result.rejected):
            self.rejected_table.setItem(r, 0, QTableWidgetItem(item.motor.model))
            self.rejected_table.setItem(r, 1, QTableWidgetItem(", ".join(item.reasons)))


def run_app() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1200, 700)
    window.show()
    return app.exec()
