from __future__ import annotations

from enum import Enum

from PyQt6.QtWidgets import QGridLayout, QWidget

from core.camera import Camera, OrbitCamera
from editor import ViewportState
from render.gl_viewport import GLViewport
from scene.scene import Scene


class ViewportGridMode(Enum):
    SINGLE = "single"
    QUAD = "quad"


class ViewportId(Enum):
    PERSPECTIVE = "perspective"
    FRONT = "front"
    TOP = "top"
    RIGHT = "right"


class ViewportGrid(QWidget):
    def __init__(
        self,
        scene: Scene,
        parent=None,
        mode: ViewportGridMode = ViewportGridMode.SINGLE,
    ):
        super().__init__(parent)

        self._scene = scene
        self._viewports: dict[ViewportId, GLViewport] = {}
        self._active_viewport_id = ViewportId.PERSPECTIVE
        self._current_viewport_mode = mode

        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(1)

        self._build_viewports()
        self._rebuild_layout()

    # --- Public API ---
    @property
    def active_viewport(self) -> GLViewport:
        return self._viewports[self._active_viewport_id]

    @property
    def viewports(self) -> tuple[GLViewport, ...]:
        return tuple(self._viewports.values())

    @property
    def current_viewport_mode(self) -> ViewportGridMode:
        return self._current_viewport_mode

    def mark_scene_dirty(self) -> None:
        for viewport in self._viewports.values():
            viewport.mark_scene_dirty()

    def set_current_camera(self, camera: Camera) -> None:
        self.active_viewport.set_current_camera(camera)

    def set_mode(self, mode: ViewportGridMode) -> None:
        if mode == self._current_viewport_mode:
            return

        self._current_viewport_mode = mode
        self._rebuild_layout()

    def toggle_mode(self) -> None:
        if self._current_viewport_mode == ViewportGridMode.QUAD:
            self.set_mode(ViewportGridMode.SINGLE)
        else:
            self.set_mode(ViewportGridMode.QUAD)

    # --- Private helpers ---
    def _build_viewports(self) -> None:
        self._viewports = {
            ViewportId.PERSPECTIVE: self._create_viewport(self._create_perspective_state()),
            ViewportId.FRONT: self._create_viewport(self._create_front_state()),
            ViewportId.TOP: self._create_viewport(self._create_top_state()),
            ViewportId.RIGHT: self._create_viewport(self._create_right_state()),
        }

    def _rebuild_layout(self) -> None:
        self._clear_layout()

        if self._current_viewport_mode == ViewportGridMode.QUAD:
            self._show_quad_layout()
        else:
            self._show_single_layout()

    def _clear_layout(self) -> None:
        while self._layout.count():
            self._layout.takeAt(0)

    def _show_single_layout(self) -> None:
        for viewport in self._viewports.values():
            viewport.hide()

        viewport = self.active_viewport
        self._layout.addWidget(viewport, 0, 0)
        viewport.show()

    def _show_quad_layout(self) -> None:
        for viewport in self._viewports.values():
            viewport.show()

        self._layout.addWidget(self._viewports[ViewportId.PERSPECTIVE], 0, 0)
        self._layout.addWidget(self._viewports[ViewportId.FRONT], 0, 1)
        self._layout.addWidget(self._viewports[ViewportId.TOP], 1, 0)
        self._layout.addWidget(self._viewports[ViewportId.RIGHT], 1, 1)

    def _create_viewport(self, state: ViewportState) -> GLViewport:
        viewport = GLViewport(self, viewport_state=state)
        viewport.set_scene(self._scene)
        return viewport

    def _create_perspective_state(self) -> ViewportState:
        camera = OrbitCamera()
        camera.set_perspective_view()
        return ViewportState(camera=camera)

    def _create_front_state(self) -> ViewportState:
        camera = OrbitCamera()
        camera.set_front_view()
        return ViewportState(camera=camera)

    def _create_top_state(self) -> ViewportState:
        camera = OrbitCamera()
        camera.set_top_view()
        return ViewportState(camera=camera)

    def _create_right_state(self) -> ViewportState:
        camera = OrbitCamera()
        camera.set_right_view()
        return ViewportState(camera=camera)
