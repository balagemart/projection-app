from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QLabel
from PyQt6.QtCore import Qt, pyqtSignal


class ControlsPanel(QWidget):

    scale_changed = pyqtSignal(int)         # event with int value

    def __init__(self):
        super().__init__()
        self.setObjectName("ControlsPanel")
        self.setAutoFillBackground(True)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Scale"))

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(10)
        self.slider.setMaximum(200)
        self.slider.setValue(100)

        layout.addWidget(self.slider)
        layout.addStretch(1)

        self.slider.valueChanged.connect(self.scale_changed.emit)
