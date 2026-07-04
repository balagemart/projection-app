from __future__ import annotations

from pathlib import Path

import OpenGL.GL as gl

from core.camera import Camera
from geometry.mesh_data import PrimitiveType
from render.axes import create_axes
from render.grid import create_grid
from render.mesh import Mesh
from render.normals import build_face_normals
from render.edges import build_edge_vetors
from scene.scene import Scene
from editor.viewport_state import ViewportState


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
    program = gl.glCreateProgram()
    gl.glAttachShader(program, vs)
    gl.glAttachShader(program, fs)
    gl.glLinkProgram(program)

    ok = gl.glGetProgramiv(program, gl.GL_LINK_STATUS)
    if not ok:
        log = gl.glGetProgramInfoLog(program).decode("utf-8", errors="replace")
        raise RuntimeError(f"Program link error:\n{log}")

    gl.glDeleteShader(vs)
    gl.glDeleteShader(fs)
    return program


class Renderer:
    def __init__(self) -> None:
        self._program: int | None = None
        self._u_mvp_loc: int = -1
        self._meshes: list[Mesh] = []
        self.grid: Mesh | None = None
        self.axes: Mesh | None = None

    def initialize(self) -> None:
        base = Path(__file__).resolve().parent
        vert_src = _read_text(base / "shaders" / "basic.vert")
        frag_src = _read_text(base / "shaders" / "basic.frag")

        vs = _compile_shader(vert_src, gl.GL_VERTEX_SHADER)
        fs = _compile_shader(frag_src, gl.GL_FRAGMENT_SHADER)
        self._program = _link_program(vs, fs)

        self._u_mvp_loc = gl.glGetUniformLocation(self._program, "u_mvp")
        if self._u_mvp_loc < 0:
            raise RuntimeError("Nem találom az 'u_mvp' uniformot a shaderben.")

        self.grid = create_grid()
        self.axes = create_axes()

        gl.glClearColor(0.27, 0.27, 0.27, 1.0)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_MULTISAMPLE)

    def rebuild_scene(self, scene: Scene) -> None:
        self._dispose_scene_meshes()

        for obj in scene.objects:
            mesh = scene.get_object_mesh(obj)
            if mesh is None:
                continue

            self._meshes.append(
                Mesh(
                    vertices=mesh.vertices,
                    components_per_vertex=mesh.components_per_vertex,
                    primitive=self._to_gl_primitive(mesh.primitive),
                    indices=mesh.indices,
                )
            )
            if (
                obj.show_normals
                and mesh.primitive == PrimitiveType.TRIANGLES
                and mesh.indices is not None
            ):
                normal_mesh = build_face_normals(
                    mesh.vertices,
                    mesh.indices,
                    mesh.components_per_vertex,
                )
                self._meshes.append(normal_mesh)
            if (
                obj.show_edges
                and mesh.primitive == PrimitiveType.TRIANGLES
                and mesh.indices is not None
            ):
                edge_mesh = build_edge_vetors(
                    mesh.vertices,
                    mesh.indices,
                    mesh.components_per_vertex
                )
                self._meshes.append(edge_mesh)

    def draw(self, state: ViewportState, aspect: float) -> None:
        if self._program is None:
            return

        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        camera = state.camera
        mvp = camera.projection_matrix(aspect) @ camera.view_matrix()

        gl.glUseProgram(self._program)
        gl.glUniformMatrix4fv(self._u_mvp_loc, 1, gl.GL_FALSE, mvp.T)

        if state.show_grid and self.grid is not None:
            self.grid.draw()
        if state.show_axes and self.axes is not None:
            self.axes.draw()
        for mesh in self._meshes:
            mesh.draw()

        gl.glUseProgram(0)

    def dispose(self) -> None:
        self._dispose_scene_meshes()

        if self.grid is not None:
            self.grid.dispose()
            self.grid = None
        if self.axes is not None:
            self.axes.dispose()
            self.axes = None
        if self._program is not None:
            gl.glDeleteProgram(self._program)
            self._program = None

        self._u_mvp_loc = -1

    def _dispose_scene_meshes(self) -> None:
        for mesh in self._meshes:
            mesh.dispose()
        self._meshes.clear()

    def _to_gl_primitive(self, primitive: PrimitiveType) -> int:
        if primitive == PrimitiveType.TRIANGLES:
            return gl.GL_TRIANGLES
        if primitive == PrimitiveType.LINES:
            return gl.GL_LINES
        raise ValueError(f"Unsupported primitive: {primitive}")
