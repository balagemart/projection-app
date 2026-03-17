from __future__ import annotations

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QFileDialog,
)

from ui.styles import DARK_THEME
from ui.left_panel import LeftPanel
from ui.right_panel import RightPanel
from ui.menus import build_menus
from scene.scene import Scene
from io_utils.obj_loader import load_obj
from render.gl_viewport import GLViewport


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

        self.left_panel = LeftPanel()
        self.left_panel.set_scene(self.scene)
        self.right_panel = RightPanel(self.scene)
        self.left_panel.scene_changed.connect(self.viewport.mark_scene_dirty)

        layout.addWidget(self.left_panel, 1)
        layout.addWidget(self.right_panel, 4)

        # --- Menus ---
        build_menus(self, on_import_obj=self._import_obj)

        # --- Wire up TopBar actions ---
        self.right_panel.top_bar.add_cube_requested.connect(self._add_cube)
        self.right_panel.top_bar.add_sphere_requested.connect(self._add_sphere)

        self.right_panel.top_bar.set_perspective_view_requested.connect(self._set_perspective_view)

        self.right_panel.top_bar.set_ortho_front_view_requested.connect(self._set_front_view)
        self.right_panel.top_bar.set_ortho_top_view_requested.connect(self._set_top_view)
        self.right_panel.top_bar.set_ortho_bottom_view_requested.connect(self._set_bottom_view)
        self.right_panel.top_bar.set_ortho_right_view_requested.connect(self._set_right_view)
        self.right_panel.top_bar.set_ortho_isom_view_requested.connect(self._set_isometric_view)
        self.right_panel.top_bar.set_scene_cam_view_requested.connect(self._set_scene_cam_view)
        self.right_panel.top_bar.add_camera_requested.connect(self._add_camera)

    @property
    def viewport(self) -> GLViewport:
        return self.right_panel.viewport

    # --- Private helpers ---
    def _set_scene_cam_view(self) -> None:
        cam = self.scene.get_selected_camera()
        if cam is not None:
            self.viewport.set_current_camera(cam)
            self._refresh_view()
        else:
            self._set_perspective_view()    # Most ez miatt ha nincs camera es ranyomsz akkor alap allasba all az edit camera

    def _set_perspective_view(self) -> None:
        self.scene.editor_camera.set_perspective_view()
        self.viewport.set_current_camera(self.scene.editor_camera)
        self._refresh_view()

    def _set_isometric_view(self) -> None:
        self.scene.editor_camera.set_isometric_view()
        self._refresh_view()

    def _set_front_view(self) -> None:
        self.scene.editor_camera.set_front_view()
        self._refresh_view()

    def _set_top_view(self) -> None:
        self.scene.editor_camera.set_top_view()
        self._refresh_view()

    def _set_bottom_view(self) -> None:
        self.scene.editor_camera.set_bottom_view()
        self._refresh_view()

    def _set_right_view(self) -> None:
        self.scene.editor_camera.set_right_view()
        self._refresh_view()

    def _add_camera(self):
        self.scene.add_camera()
        self.left_panel.refresh_objects()
        self._refresh_view()

    def _add_cube(self) -> None:
        self.scene.add_cube()
        self.left_panel.refresh_objects()
        self._refresh_view()

    def _add_sphere(self) -> None:
        self.scene.add_sphere()
        self.left_panel.refresh_objects()
        self._refresh_view()

    def _import_obj(self) -> None:  # TODO atirni mar mashogy mukodik a scene
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
        self._refresh_view()

    def _refresh_view(self) -> None:
        self.viewport.mark_scene_dirty()
