import pickle

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

import settings


class MedianFilterGroup(QGroupBox):
    def __init__(self):
        super().__init__("Медианный фильтр")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.enable = QCheckBox(
            "Активировать фильтр", checked=settings.MEDIAN_FILTER_DEFAULT_APPLY
        )

        self.window_x = QSpinBox()
        self.window_x.setRange(1, 1000)
        self.window_x.setValue(settings.MEDIAN_FILTER_DEFAULT_WINDOW_SHAPE[0])
        self.window_y = QSpinBox()
        self.window_y.setRange(1, 1000)
        self.window_y.setValue(settings.MEDIAN_FILTER_DEFAULT_WINDOW_SHAPE[1])

        window_shape_layout = QHBoxLayout()
        window_shape_layout.addWidget(QLabel("Размер окна:"))
        window_shape_layout.addWidget(self.window_x)
        window_shape_layout.addWidget(QLabel("x"))
        window_shape_layout.addWidget(self.window_y)

        self.pad_mode = QComboBox()
        self.pad_mode.addItems(["edge", "constant", "reflect"])
        self.pad_mode.setCurrentText(settings.MEDIAN_FILTER_DEFAULT_PAD_MODE)

        layout.addWidget(self.enable)
        layout.addLayout(window_shape_layout)
        layout.addWidget(QLabel("Режим заполнения:"))
        layout.addWidget(self.pad_mode)
        self.setLayout(layout)

    def get_params(self):
        return {
            "apply": self.enable.isChecked(),
            "window_shape": (self.window_x.value(), self.window_y.value()),
            "pad_mode": self.pad_mode.currentText(),
        }


class MovingAverageGroup(QGroupBox):
    def __init__(self):
        super().__init__("Скользящее среднее")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.enable = QCheckBox(
            "Активировать фильтр", checked=settings.MOVING_AVERAGE_DEFAULT_APPLY
        )
        self.window = QSpinBox()
        self.window.setRange(1, 100)
        self.window.setValue(settings.MOVING_AVERAGE_DEFAULT_WINDOW_SIZE)

        self.axis = QComboBox()
        self.axis.addItems(["0 (X)", "1 (Y)", "2 (Z)"])
        self.axis.setCurrentIndex(settings.MOVING_AVERAGE_DEFAULT_AXIS)

        self.mode = QComboBox()
        self.mode.addItems(["same", "valid", "full"])
        self.mode.setCurrentText(settings.MOVING_AVERAGE_DEFAULT_MODE)

        self.window_type = QComboBox()
        self.window_type.addItems(["gaussian", "uniform"])
        self.window_type.setCurrentText(settings.MOVING_AVERAGE_DEFAULT_WINDOW_TYPE)

        layout.addWidget(self.enable)
        layout.addWidget(QLabel("Размер окна:"))
        layout.addWidget(self.window)
        layout.addWidget(QLabel("Ось применения:"))
        layout.addWidget(self.axis)
        layout.addWidget(QLabel("Режим вычислений:"))
        layout.addWidget(self.mode)
        layout.addWidget(QLabel("Тип окна:"))
        layout.addWidget(self.window_type)
        self.setLayout(layout)

    def get_params(self):
        return {
            "apply": self.enable.isChecked(),
            "window_size": self.window.value(),
            "axis": self.axis.currentIndex(),
            "mode": self.mode.currentText(),
            "window_type": self.window_type.currentText(),
        }


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Фильтры обработки сигналов")
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        self.mf_group = MedianFilterGroup()
        self.ma_group = MovingAverageGroup()

        apply_btn = QPushButton("Применить параметры")
        apply_btn.clicked.connect(self.apply_settings)

        main_layout.addWidget(QLabel("Сервер запущен"))
        main_layout.addWidget(self.mf_group)
        main_layout.addWidget(self.ma_group)
        main_layout.addWidget(apply_btn)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def apply_settings(self):
        params = {
            "moving_average": self.ma_group.get_params(),
            "median_filter": self.mf_group.get_params(),
        }
        pickle.dump(params, open(settings.FILTERS_PARAMS_PATH, "wb"))
