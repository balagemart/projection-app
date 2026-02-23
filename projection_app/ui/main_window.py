from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel
)

from render.gl_viewport import GLViewport
from ui.controls_panel import ControlsPanel
from ui.styles import DARK_THEME
from scene.scene import Scene

# MainLayout (HBox)
# ├── ControlsPanel
# └── Right (VBox)
#        ├── TopBar
#        └── Viewport


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Projection App")
        self.setStyleSheet(DARK_THEME)

        # Root (central widget)
        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left side – Controls panel
        self.controls = ControlsPanel()
        main_layout.addWidget(self.controls, 1)

        # Right side container
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # ---- Top bar ----
        top_bar = QWidget()
        top_bar.setObjectName("ViewportBar")
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(8, 6, 8, 6)

        top_layout.addWidget(QLabel("Viewport Bar"))

        # ---- Viewport ----
        self.viewport = GLViewport()
        # Scene (világállapot)
        self.scene = Scene()
        self.viewport.scene = self.scene

        right_layout.addWidget(top_bar)
        right_layout.addWidget(self.viewport, 1)  # 1 = stretch

        main_layout.addWidget(right, 4)

        # UI → Render kapcsolat
        self.controls.scale_changed.connect(
            self.viewport.set_scale_from_slider
        )
