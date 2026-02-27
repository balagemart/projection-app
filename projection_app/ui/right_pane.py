from __future__ import annotations

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from render.gl_viewport import GLViewport
from scene.scene import Scene
from ui.top_bar import TopBar


class RightPane(QWidget):
    def __init__(self, scene: Scene, parent=None):
        super().__init__(parent)
        self.setObjectName("RightPane")
        self.top_bar = TopBar(self)
        self.viewport = GLViewport(self)
        self.viewport.scene = scene  # összekötés

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.top_bar)
        layout.addWidget(self.viewport, 1)
