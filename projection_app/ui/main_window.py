from __future__ import annotations

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QFileDialog,
)

from ui.styles import DARK_THEME
from ui.controls_panel import ControlsPanel
from ui.right_pane import RightPane
from ui.menus import build_menus

from scene.scene import Scene
from io_utils.obj_loader import load_obj
from models.sphere import sphere_vertices
from models.cube import cube_vertices_per_vertex_colors, cube_indices


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
        self.right_pane = RightPane(self.scene)

        layout.addWidget(self.left_panel, 1)
        layout.addWidget(self.right_pane, 4)

        # --- Menus ---
        build_menus(self, on_import_obj=self.import_obj)

        # --- Wire up TopBar actions ---
        self.right_pane.top_bar.add_cube_requested.connect(self.add_cube)
        self.right_pane.top_bar.add_sphere_requested.connect(self.add_sphere)

        # (ha a ControlsPanel küld jelet, itt kötöd össze a viewporttal)
        # self.left_panel.scale_changed.connect(self.right_pane.viewport.set_scale_from_slider)

    @property
    def viewport(self):
        return self.right_pane.viewport

    def import_obj(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Import OBJ",
            "",
            "OBJ Files (*.obj)",
        )
        if not path:
            return

        verts, inds = load_obj(path)

        self.scene.clear_meshes()
        # OBJ általában xyz (3)
        self.scene.add_mesh(verts, inds, components_per_vertex=3)

        self.viewport.mark_scene_dirty()

    def add_cube(self) -> None:
        verts = cube_vertices_per_vertex_colors(size=3.0)
        inds = cube_indices()

        self.scene.add_mesh(verts, inds, components_per_vertex=6)
        self.viewport.mark_scene_dirty()

    def add_sphere(self) -> None:
        verts, inds = sphere_vertices(2, 100, 100)
        verts = verts.reshape(-1)

        # Ha a sphere jelenleg xyz-only: 3
        self.scene.add_mesh(verts, inds, components_per_vertex=6)
        self.viewport.mark_scene_dirty()
