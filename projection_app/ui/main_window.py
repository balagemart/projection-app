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

        # Main panel
        main_panel = QWidget()
        main_layout = QHBoxLayout(main_panel)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setCentralWidget(main_panel)

        # Left panel
        self.left_panel = ControlsPanel()
        main_layout.addWidget(self.left_panel, 1)

        # Right panel
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        main_layout.addWidget(right_panel, 4)

        # Rp - Top bar
        top_bar = QWidget()
        top_layout = QHBoxLayout(top_bar)
        top_layout.setContentsMargins(8, 6, 8, 6)
        right_layout.addWidget(top_bar)

        # Rp - Bottom bar (Viewport)
        self.viewport = GLViewport()
        self.scene = Scene()
        self.viewport.scene = self.scene
        right_layout.addWidget(self.viewport, 1)

