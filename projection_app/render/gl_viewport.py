from __future__ import annotations
from pathlib import Path
from enum import Enum

from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt
import numpy as np
import OpenGL.GL as gl

from render.mesh import Mesh
from render.grid import create_grid
from render.axes import create_axes
from render.normals import build_face_normals
from scene.scene import Scene, SceneObject, PrimitiveType
from core.camera import ViewMode, OrbitCamera
from core.transforms import look_at, perspective, orthographic, identity
from core.camera import ProjectionMode


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _compile_shader(src: str, shader_type: int) -> int:
    shader = gl.glCreateShader(shader_type)
    gl.glShaderSource(shader, src)
    gl.glCompileShader(shader)

    ok = gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS)
    if not ok:
        log = gl.glGetShaderInfoLog(shader).decode("utf-8", errors="replace")
        raise RuntimeError(f"Shader compile error:\n{log}")
    return shader


def _link_program(vs: int, fs: int) -> int:
    prog = gl.glCreateProgram()
    gl.glAttachShader(prog, vs)
    gl.glAttachShader(prog, fs)
    gl.glLinkProgram(prog)

    ok = gl.glGetProgramiv(prog, gl.GL_LINK_STATUS)
    if not ok:
        log = gl.glGetProgramInfoLog(prog).decode("utf-8", errors="replace")
        raise RuntimeError(f"Program link error:\n{log}")

    gl.glDeleteShader(vs)
    gl.glDeleteShader(fs)
    return prog


class GLViewport(QOpenGLWidget):
    """
    OpenGL viewport Qt-n belül.
    - Qt adja az OpenGL contextet
    - shader init initializeGL-ben
    - a Scene mesh-eiből GPU Mesh-eket épít (rebuild)
    - paintGL-ben rajzol
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(640, 480)
        self.setObjectName("ViewPort")

        # --- GL state ---
        self._program: int | None = None
        self._u_mvp_loc: int = -1

        # --- Scene ---
        self._scene: Scene | None = None
        self._current_camera: OrbitCamera | SceneObject = None

        # --- Rendered meshes (GPU oldali) ---
        self._meshes: list[Mesh] = []
        self._scene_dirty: bool = True

        # --- Input state ---
        self._last_pos = None

        # --- Overlays (viewport segédek) ---
        self.grid: Mesh | None = None
        self.axes: Mesh | None = None

    @property
    def editor_camera(self) -> OrbitCamera:
        if self._scene is None:
            raise RuntimeError("GLViewport.scene nincs beállítva.")
        return self._scene.editor_camera

    # --- Qt OpenGL lifecycle ---
    def initializeGL(self) -> None:
        base = Path(__file__).resolve().parent
        vert_src = _read_text(base / "shaders" / "basic.vert")
        frag_src = _read_text(base / "shaders" / "basic.frag")

        vs = _compile_shader(vert_src, gl.GL_VERTEX_SHADER)
        fs = _compile_shader(frag_src, gl.GL_FRAGMENT_SHADER)
        self._program = _link_program(vs, fs)

        self._u_mvp_loc = gl.glGetUniformLocation(self._program, "u_mvp")
        if self._u_mvp_loc < 0:
            raise RuntimeError("Nem találom az 'u_mvp' uniformot a shaderben.")

        # Viewport overlay-k
        self.grid = create_grid()
        self.axes = create_axes()

        gl.glClearColor(0.27, 0.27, 0.27, 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_MULTISAMPLE)

        # Ha induláskor már van Scene tartalom, építsük fel
        self._scene_dirty = True

    def resizeGL(self, w: int, h: int) -> None:
        gl.glViewport(0, 0, w, h)

    def paintGL(self) -> None:
        # Itt biztosan van aktív GL context
        if self._program is None or self._scene is None:
            return

        if self._scene_dirty:
            self._rebuild_meshes_from_scene()
            self._scene_dirty = False

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        w, h = self.width(), self.height()
        aspect = w / max(1.0, float(h))

        cam = self._current_camera
        if cam is None:
            return

        if isinstance(cam, OrbitCamera):
            mvp = cam.mvp(aspect, model=None)
        else:
            mvp = self._build_scene_camera_mvp(cam, aspect)

        gl.glUseProgram(self._program)
        gl.glUniformMatrix4fv(self._u_mvp_loc, 1, gl.GL_FALSE, mvp.T)

        # overlays
        if self.grid is not None:
            self.grid.draw()
        if self.axes is not None:
            self.axes.draw()

        # scene meshes
        for m in self._meshes:
            m.draw()

        gl.glUseProgram(0)

    # --- Public Scene API ---
    def set_scene(self, scene: Scene) -> None:
        self._scene = scene
        self._current_camera = scene.editor_camera
        self._scene_dirty = True
        self.update()

    def mark_scene_dirty(self) -> None:
        self._scene_dirty = True
        self.update()

    def set_current_camera(self, cam: OrbitCamera | SceneObject) -> None:
        self._current_camera = cam
        self.update()

    # --- Private helper ---
    def _rebuild_meshes_from_scene(self) -> None:
        """
        Scene → GPU Mesh-ek
        Csak paintGL/initializeGL alatt hívd (amikor van GL context).
        """
        self._meshes.clear()

        # scene biztosan nem None itt
        if self._scene is None:
            return

        for obj in self._scene.objects:
            mesh = obj.get_mesh()

            if mesh is None:
                continue
            verts = mesh.vertices
            inds = mesh.indices
            components_per_vertex = mesh.components_per_vertex
            primitive = self._to_gl_primitive(mesh.primitive)

            self._meshes.append(
                Mesh(
                    vertices=verts,
                    components_per_vertex=components_per_vertex,
                    primitive=primitive,
                    indices=inds,
                )
            )
            if obj.show_normals:
                normal_mesh = build_face_normals(verts, inds, components_per_vertex)
                self._meshes.append(normal_mesh)

    def _to_gl_primitive(self, primitive: PrimitiveType):
        if primitive == PrimitiveType.TRIANGLES:
            return gl.GL_TRIANGLES
        elif primitive == PrimitiveType.LINES:
            return gl.GL_LINES
        else:
            raise ValueError(f"Unsupported primitive: {primitive}")

    def _build_scene_camera_mvp(
        self,
        camera_obj: SceneObject,
        aspect: float
    ) -> np.ndarray:
        position = np.array(camera_obj.position, dtype=np.float32)
        rotation = np.array(camera_obj.rotation, dtype=np.float32)

        rx, ry, rz = rotation

        # Előrenéző irány kiszámítása Euler szögekből
        cx, sx = np.cos(rx), np.sin(rx)
        cy, sy = np.cos(ry), np.sin(ry)

        forward = np.array([
            sy * cx,
            -sx,
            cy * cx,
        ], dtype=np.float32)

        target = position + forward
        up = np.array([0.0, 1.0, 0.0], dtype=np.float32)

        view = look_at(position, target, up)

        projection_mode = camera_obj.params["projection_mode"]
        near = float(camera_obj.params["near"])
        far = float(camera_obj.params["far"])

        if projection_mode == ProjectionMode.PERSPECTIVE:
            fov_y = float(camera_obj.params["fov_y"])
            projection = perspective(
                np.deg2rad(fov_y),
                aspect,
                near,
                far,
            )
        else:
            ortho_scale = float(camera_obj.params["ortho_scale"])
            half_h = ortho_scale
            half_w = half_h * aspect

            projection = orthographic(
                -half_w,
                half_w,
                -half_h,
                half_h,
                near,
                far,
            )

        return projection @ view

    # --- Input events ---
    def mousePressEvent(self, event) -> None:
        self._last_pos = event.position()

    def mouseMoveEvent(self, event) -> None:
        if self._last_pos is None:
            return

        dx = event.position().x() - self._last_pos.x()
        dy = event.position().y() - self._last_pos.y()
        self._last_pos = event.position()

        cam = self._current_camera
        if isinstance(cam, OrbitCamera):
            if event.buttons() & Qt.MouseButton.RightButton:
                if cam.view_mode == ViewMode.FREE:
                    cam.orbit(dx, dy, sens=0.01)
                    self.update()

    def wheelEvent(self, event) -> None:
        cam = self._current_camera
        if isinstance(cam, OrbitCamera):
            cam.zoom_wheel(event.angleDelta().y())
            self.update()
