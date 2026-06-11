from __future__ import annotations

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from scene.scene import Scene
from ui.top_bar import TopBar
from ui.viewport_grid import ViewportGrid
from render.gl_viewport import GLViewport


class RightPanel(QWidget):
    def __init__(self, scene: Scene, parent=None):
        super().__init__(parent)
        self.setObjectName("RightPane")

        self.top_bar = TopBar(self)
        self.viewport_grid = ViewportGrid(scene, self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.top_bar)
        layout.addWidget(self.viewport_grid, 1)

    @property
    def viewport(self) -> GLViewport:
        return self.viewport_grid.active_viewport

    def set_viewport_grid_mode_toggle(self) -> None:
        self.viewport_grid.toggle_mode()
