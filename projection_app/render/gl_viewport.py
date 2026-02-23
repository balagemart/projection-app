from __future__ import annotations
from pathlib import Path

from PyQt6.QtOpenGLWidgets import QOpenGLWidget

import OpenGL.GL as gl

from render.mesh import Mesh

from PyQt6.QtCore import Qt

from core.camera import OrbitCamera
from render.grid import create_grid
from render.axes import create_axes
# from models.triangle import triangle_vertices
from models.cube import cube_vertices_per_vertex_colors, cube_indices
from scene.scene import Scene

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

    # A link után a külön shader objektumok már nem kellenek
    gl.glDeleteShader(vs)
    gl.glDeleteShader(fs)
    return prog


class GLViewport(QOpenGLWidget):
    """
    OpenGL viewport Qt-n belül.
    - Qt adja az OpenGL contextet
    - itt shader program + mesh init
    - paintGL-ben rajzolas
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(640, 480)

        self._program: int | None = None
        self._u_scale_loc: int = -1

        self._mesh: Mesh | None = None
        self._scale: float = 1.0

        # self.camera = OrbitCamera()
        self.scene: Scene | None = None
        self.last_pos = None

        self.grid = None
        self.axes = None

    @property
    def camera(self):
        if self.scene is None:
            raise RuntimeError("GLViewport.scene nincs beállítva (Scene hiányzik).")
        return self.scene.camera

    # --- API a UI felől ---
    def set_scale_from_slider(self, value: int) -> None:
        # slider 10..200 -> 0.10..2.00
        self._scale = value / 100.0
        self.update()

    # --- Qt OpenGL lifecycle ---
    def initializeGL(self) -> None:
        # 1) shader fájlok betöltése
        base = Path(__file__).resolve().parent
        vert_src = _read_text(base / "shaders" / "basic.vert")
        frag_src = _read_text(base / "shaders" / "basic.frag")

        # 2) compile + link
        vs = _compile_shader(vert_src, gl.GL_VERTEX_SHADER)
        fs = _compile_shader(frag_src, gl.GL_FRAGMENT_SHADER)
        self._program = _link_program(vs, fs)

        # 3) uniform location
        self._u_mvp_loc = gl.glGetUniformLocation(self._program, "u_mvp")
        if self._u_mvp_loc < 0:
            raise RuntimeError("Nem találom az 'u_mvp' uniformot a shaderben.")
        verts = cube_vertices_per_vertex_colors(size=5.0)
        inds = cube_indices()

        self._mesh = Mesh(
            vertices=verts,
            components_per_vertex=6,
            primitive=gl.GL_TRIANGLES,
            indices=inds,
        )

        # 4. grid és tengelyek
        self.grid = create_grid()
        self.axes = create_axes()

        # háttérszín
        gl.glClearColor(0.27, 0.27, 0.27, 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)

        gl.glEnable(gl.GL_MULTISAMPLE)

    def mousePressEvent(self, event):
        self.last_pos = event.position()

    def mouseMoveEvent(self, event):
        if self.last_pos is None:
            return
        dx = event.position().x() - self.last_pos.x()
        dy = event.position().y() - self.last_pos.y()
        self.last_pos = event.position()

        if event.buttons() & Qt.MouseButton.RightButton:
            self.camera.orbit(dx, dy, sens=0.01)
            self.update()

    def wheelEvent(self, event):
        self.camera.zoom_wheel(event.angleDelta().y())
        self.update()

    def resizeGL(self, w: int, h: int) -> None:
        gl.glViewport(0, 0, w, h)

    def paintGL(self) -> None:
        if self._program is None or self._mesh is None:
            return

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        w, h = self.width(), self.height()
        aspect = w / max(1.0, float(h))

        mvp = self.camera.mvp(aspect)

        gl.glUseProgram(self._program)
        gl.glUniformMatrix4fv(self._u_mvp_loc, 1, gl.GL_FALSE, mvp.T)

        if self.grid:
            self.grid.draw()
        else:
            print("Grid did not initialize.")
        if self.axes:
            # lo, hi = gl.glGetFloatv(gl.GL_ALIASED_LINE_WIDTH_RANGE)
            # gl.glLineWidth(min(1.5, float(hi)))
            self.axes.draw()
            # gl.glLineWidth(1.0)
        else:
            print("Axes did not initialize.")
        self._mesh.draw()

        gl.glUseProgram(0)
