from __future__ import annotations

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QFileDialog,
)

from ui.styles import DARK_THEME
from ui.controls_panel import ControlsPanel
from ui.right_panel import RightPanel
from ui.menus import build_menus

from scene.scene import Scene
from io_utils.obj_loader import load_obj


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projection App")
        self.setStyleSheet(DARK_THEME)

        # --- Scene ---
        self.scene = Scene()

        # --- Central layout ---
        root = QWidget(self)
        self.setCentralWidget(root)

        layout = QHBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.left_panel = ControlsPanel()
        self.left_panel.set_scene(self.scene)
        self.right_panel = RightPanel(self.scene)
        self.left_panel.scene_changed.connect(self.right_panel.viewport.mark_scene_dirty)

        layout.addWidget(self.left_panel, 1)
        layout.addWidget(self.right_panel, 4)

        # --- Menus ---
        build_menus(self, on_import_obj=self.import_obj)

        # --- Wire up TopBar actions ---
        self.right_panel.top_bar.add_cube_requested.connect(self.add_cube)
        self.right_panel.top_bar.add_sphere_requested.connect(self.add_sphere)

    @property
    def viewport(self):
        return self.right_panel.viewport

    def add_cube(self):
        self.scene.add_cube()
        self.left_panel.refresh_objects()
        self.viewport.mark_scene_dirty()

    def add_sphere(self):
        self.scene.add_sphere()
        self.left_panel.refresh_objects()
        self.viewport.mark_scene_dirty()

    def import_obj(self) -> None:  # TODO atirni mar mashogy mukodik a scene
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Import OBJ",
            "",
            "OBJ Files (*.obj)",
        )
        if not path:
            return

        verts, inds = load_obj(path)

        self.scene.add_imported(verts, inds, components_per_vertex=3)
        self.left_panel.refresh_objects()
        self.viewport.mark_scene_dirty()
