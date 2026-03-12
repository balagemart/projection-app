from __future__ import annotations

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QToolButton, QMenu, QPushButton
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal


class TopBar(QWidget):
    add_cube_requested = pyqtSignal()
    add_sphere_requested = pyqtSignal()
    set_perspective_view_requested = pyqtSignal()
    set_ortho_front_view_requested = pyqtSignal()
    set_ortho_top_view_requested = pyqtSignal()
    set_ortho_bottom_view_requested = pyqtSignal()
    set_ortho_right_view_requested = pyqtSignal()
    set_ortho_isom_view_requested = pyqtSignal()

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

        # View selector
        persp_btn = QPushButton(self)
        persp_btn.setText("Perspective")

        persp_btn.clicked.connect(self.set_perspective_view_requested.emit)

        ortho_btn = QToolButton(self)
        ortho_btn.setText("Orthographic")
        ortho_btn.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)

        ortho_menu = QMenu(ortho_btn)

        act_front_view = QAction("Front", self)
        act_front_view.triggered.connect(self.set_ortho_front_view_requested.emit)

        act_top_view = QAction("Top", self)
        act_top_view.triggered.connect(self.set_ortho_top_view_requested.emit)

        act_bottom_view = QAction("Bottom", self)
        act_bottom_view.triggered.connect(self.set_ortho_bottom_view_requested.emit)

        act_right_view = QAction("Right", self)
        act_right_view.triggered.connect(self.set_ortho_right_view_requested.emit)

        act_isom_view = QAction("Isometric", self)
        act_isom_view.triggered.connect(self.set_ortho_isom_view_requested.emit)

        ortho_menu.addAction(act_front_view)
        ortho_menu.addAction(act_top_view)
        ortho_menu.addAction(act_bottom_view)
        ortho_menu.addAction(act_right_view)
        ortho_menu.addAction(act_isom_view)
        ortho_btn.setMenu(ortho_menu)

        layout.addWidget(persp_btn)
        layout.addWidget(ortho_btn)

        layout.addStretch(1)
