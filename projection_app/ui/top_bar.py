from __future__ import annotations

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QToolButton, QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal


class TopBar(QWidget):
    add_cube_requested = pyqtSignal()
    add_sphere_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TopBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(8)

        # Geometry dropdown
        geom_btn = QToolButton(self)
        geom_btn.setText("Geometry")
        geom_btn.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        geom_menu = QMenu(geom_btn)

        act_cube = QAction("Cube", self)
        act_cube.triggered.connect(self.add_cube_requested.emit)

        act_sphere = QAction("Sphere", self)
        act_sphere.triggered.connect(self.add_sphere_requested.emit)

        geom_menu.addAction(act_cube)
        geom_menu.addAction(act_sphere)
        geom_btn.setMenu(geom_menu)

        layout.addWidget(geom_btn)
        layout.addStretch(1)
