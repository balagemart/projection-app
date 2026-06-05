from __future__ import annotations

from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
import OpenGL.GL as gl

from render.renderer import Renderer
from scene.scene import Scene
from core.camera import Camera, ViewMode, OrbitCamera
from editor.viewport_state import ViewportState


class GLViewport(QOpenGLWidget):
    """
    OpenGL viewport Qt-n belül.
    - Qt adja az OpenGL contextet
    - shader init initializeGL-ben
    - a Scene mesh-eiből GPU Mesh-eket épít (rebuild)
    - paintGL-ben rajzol
    """

    def __init__(self, parent=None, viewport_state: ViewportState | None = None):
        super().__init__(parent)
        self.setMinimumSize(640, 480)
        self.setObjectName("ViewPort")
        self._renderer = Renderer()

        # --- Scene ---
        self._scene: Scene | None = None
        self._viewport_state = viewport_state

        self._scene_dirty: bool = True

        # --- Input state ---
        self._last_pos = None

    @property
    def editor_camera(self) -> OrbitCamera:
        if self._scene is None:
            raise RuntimeError("GLViewport.scene nincs beállítva.")
        return self._scene.editor_camera

    @property
    def state(self) -> ViewportState | None:
        return self._viewport_state

    # --- Qt OpenGL lifecycle ---
    def initializeGL(self) -> None:
        self._renderer.initialize()

    def resizeGL(self, w: int, h: int) -> None:
        gl.glViewport(0, 0, w, h)

    def paintGL(self) -> None:
        # Itt biztosan van aktív GL context
        if self._scene is None or self._viewport_state is None:
            return

        if self._scene_dirty:
            self._renderer.rebuild_scene(self._scene)
            self._scene_dirty = False

        w, h = self.width(), self.height()
        aspect = w / max(1.0, float(h))

        self._renderer.draw(self._viewport_state, aspect)

    # --- Public Scene API ---
    def set_scene(self, scene: Scene) -> None:
        self._scene = scene

        if self._viewport_state is None:
            self._viewport_state = ViewportState(camera=scene.editor_camera)

        self._scene_dirty = True
        self.update()

    def mark_scene_dirty(self) -> None:
        self._scene_dirty = True
        self.update()

    def set_current_camera(self, camera: Camera) -> None:
        if self._viewport_state is None:
            self._viewport_state = ViewportState(camera=camera)
        else:
            self._viewport_state.camera = camera

        self.update()

    def closeEvent(self, event) -> None:
        self.makeCurrent()
        self._renderer.dispose()
        self.doneCurrent()
        super().closeEvent(event)

    # --- Input events ---
    def mousePressEvent(self, event) -> None:
        self._last_pos = event.position()

    def mouseMoveEvent(self, event) -> None:
        if self._last_pos is None:
            return

        dx = event.position().x() - self._last_pos.x()
        dy = event.position().y() - self._last_pos.y()
        self._last_pos = event.position()

        cam = self._viewport_state.camera if self._viewport_state is not None else None
        if isinstance(cam, OrbitCamera):
            if event.buttons() & Qt.MouseButton.RightButton:
                if cam.view_mode == ViewMode.FREE:
                    cam.orbit(dx, dy, sens=0.01)
                    self.update()

    def wheelEvent(self, event) -> None:
        cam = self._viewport_state.camera if self._viewport_state is not None else None
        if isinstance(cam, OrbitCamera):
            cam.zoom_wheel(event.angleDelta().y())
            self.update()
