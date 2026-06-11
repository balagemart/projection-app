from __future__ import annotations

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from core.camera import Camera
from render.gl_viewport import GLViewport
from scene.scene import Scene

class ViewportGrid(QWidget):
    def __init__(self, scene: Scene, parent=None):
        super().__init__(parent)

