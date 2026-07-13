from __future__ import annotations

from contextlib import contextmanager
import time

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
from ui.viewport_grid import ViewportGrid
from scene.scene import Scene
from scene.factories import create_camera, create_cube, create_imported_mesh, create_sphere, create_point, create_line_between, create_frustum
from scene.entity import ObjectType
from io_utils.obj_loader import load_obj


@contextmanager
def timer(name: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"{name}: {end - start:.4f} s")


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
        self.left_panel.setFixedWidth(280)
        self.left_panel.set_scene(self.scene)
        self.right_panel = RightPanel(self.scene)
        self.left_panel.scene_changed.connect(self.viewport_grid.mark_scene_dirty)

        layout.addWidget(self.left_panel, 1)
        layout.addWidget(self.right_panel, 4)

        # --- Menus ---
        build_menus(self, on_import_obj=self._import_obj)

        # --- Wire up TopBar actions ---
        self.right_panel.top_bar.add_cube_requested.connect(self._add_cube)
        self.right_panel.top_bar.add_sphere_requested.connect(self._add_sphere)
        self.right_panel.top_bar.add_point_requested.connect(self._add_point)
        self.right_panel.top_bar.add_camera_requested.connect(self._add_camera)
        self.right_panel.top_bar.add_frustum_requested.connect(self._add_frustum)
        self.right_panel.top_bar.connect_selected_requested.connect(self._connect_selected)

        self.right_panel.top_bar.set_perspective_view_requested.connect(self._set_perspective_view)

        self.right_panel.top_bar.set_ortho_front_view_requested.connect(self._set_front_view)
        self.right_panel.top_bar.set_ortho_top_view_requested.connect(self._set_top_view)
        self.right_panel.top_bar.set_ortho_bottom_view_requested.connect(self._set_bottom_view)
        self.right_panel.top_bar.set_ortho_right_view_requested.connect(self._set_right_view)
        self.right_panel.top_bar.set_ortho_isom_view_requested.connect(self._set_isometric_view)
        self.right_panel.top_bar.set_scene_cam_view_requested.connect(self._set_scene_cam_view)
        self.right_panel.top_bar.set_multi_view_toggle_requested.connect(self._set_multi_view_toggle_requested)

        self.right_panel.top_bar.intersect_requested.connect(self._intersect)

    @property
    def viewport_grid(self) -> ViewportGrid:
        return self.right_panel.viewport_grid

    # --- Private helpers ---
    def _intersect(self) -> None:
        with timer("make_intersections"):
            self.scene.make_intersections()
        self._refresh_view()

    def _set_multi_view_toggle_requested(self) -> None:
        self.right_panel.set_viewport_grid_mode_toggle()

    def _set_scene_cam_view(self) -> None:
        cam = self.scene.get_selected_camera()
        if cam is not None and cam.camera is not None:
            self.viewport_grid.set_current_camera(cam.camera)
            self._refresh_view()
        else:
            self._set_perspective_view()    # Most ez miatt ha nincs camera es ranyomsz akkor alap allasba all az edit camera

    def _set_perspective_view(self) -> None:
        self.scene.editor_camera.set_perspective_view()
        self.viewport_grid.set_current_camera(self.scene.editor_camera)
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
        self.scene.add_object(create_camera())
        self.left_panel.refresh_objects()
        self._refresh_view()

    def _add_cube(self) -> None:
        self.scene.add_object(create_cube())
        self.left_panel.refresh_objects()
        self._refresh_view()

    def _add_sphere(self) -> None:
        self.scene.add_object(create_sphere())
        self.left_panel.refresh_objects()
        self._refresh_view()

    def _add_point(self) -> None:
        self.scene.add_object(create_point())
        self.left_panel.refresh_objects()
        self._refresh_view()

    def _connect_selected(self) -> None:
        selected_ids = self.left_panel.selected_object_ids()

        if len(selected_ids) != 2:
            return

        start_obj = self.scene.get_object(selected_ids[0])
        end_obj = self.scene.get_object(selected_ids[1])

        if start_obj is None or end_obj is None:
            return

        if start_obj.obj_type != ObjectType.POINT or end_obj.obj_type != ObjectType.POINT:
            return

        self.scene.add_object(create_line_between(start_obj.id, end_obj.id))
        self.left_panel.refresh_objects()
        self._refresh_view()

    def _add_frustum(self) -> None:
        selected_ids = self.left_panel.selected_object_ids()
        if len(selected_ids) != 1:
            return

        obj = self.scene.get_object(selected_ids[0])
        if obj is None or obj.camera is None or obj.obj_type != ObjectType.CAMERA:
            return

        aspect = obj.camera.aspect

        self.scene.add_object(create_frustum(obj.camera, aspect))
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

        self.scene.add_object(
            create_imported_mesh(verts, inds, components_per_vertex=3)
        )
        self.left_panel.refresh_objects()
        self._refresh_view()

    def _refresh_view(self) -> None:
        self.viewport_grid.mark_scene_dirty()
