from __future__ import annotations

import ctypes
from dataclasses import dataclass
import numpy as np
import OpenGL.GL as gl


@dataclass
class VertexLayout:
    """
    Egyszerű layout leírás:
    - position: mindig location 0 (vec3)
    - ha components_per_vertex == 6: color is van location 1 (vec3)
    """
    components_per_vertex: int = 3  # 3: xyz, 6: xyz rgb


class Mesh:
    """
    Mesh VAO+VBO (+ opcionális EBO).

    vertices: flat float32 array
      - 3 komponens: x y z
      - 6 komponens: x y z r g b

    indices: optional uint32 array
      - ha megadod: glDrawElements
      - ha nincs: glDrawArrays
    """

    def __init__(
        self,
        vertices: np.ndarray,
        components_per_vertex: int = 3,
        primitive: int = gl.GL_TRIANGLES,
        indices: np.ndarray | None = None,
    ):
        # --- vertices normalize ---
        if vertices.dtype != np.float32:
            vertices = vertices.astype(np.float32, copy=False)

        if components_per_vertex not in (3, 6):
            raise ValueError("components_per_vertex must be 3 or 6")

        self._components = components_per_vertex
        self._primitive = primitive

        # --- indices normalize ---
        self._has_indices = indices is not None
        self._index_count = 0
        self._index_type = None  # gl.GL_UNSIGNED_INT

        if self._has_indices:
            if indices.dtype != np.uint32:
                indices = indices.astype(np.uint32, copy=False)
            self._index_count = int(indices.size)
            self._index_type = gl.GL_UNSIGNED_INT
        else:
            self._vertex_count = int(len(vertices) / components_per_vertex)

        # --- GPU objects ---
        self._vao = gl.glGenVertexArrays(1)
        self._vbo = gl.glGenBuffers(1)
        self._ebo = gl.glGenBuffers(1) if self._has_indices else None

        gl.glBindVertexArray(self._vao)

        # VBO upload
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self._vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)

        # EBO upload (fontos: EBO binding VAO-hoz kötött state!)
        if self._has_indices:
            assert self._ebo is not None
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, self._ebo)
            gl.glBufferData(
                gl.GL_ELEMENT_ARRAY_BUFFER,
                indices.nbytes,
                indices,
                gl.GL_STATIC_DRAW,
            )

        # attrib 0: position vec3
        stride = self._components * 4  # float32 byte size
        gl.glEnableVertexAttribArray(0)
        gl.glVertexAttribPointer(
            0, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, ctypes.c_void_p(0)
        )

        # attrib 1: color vec3 (ha van)
        if self._components == 6:
            gl.glEnableVertexAttribArray(1)
            gl.glVertexAttribPointer(
                1, 3, gl.GL_FLOAT, gl.GL_FALSE, stride, ctypes.c_void_p(3 * 4)
            )
        else:
            gl.glDisableVertexAttribArray(1)
            gl.glVertexAttrib3f(1, 0.8, 0.8, 0.8)

        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)

    def draw(self) -> None:
        gl.glBindVertexArray(self._vao)
        if self._has_indices:
            gl.glDrawElements(self._primitive, self._index_count, self._index_type, ctypes.c_void_p(0))
        else:
            gl.glDrawArrays(self._primitive, 0, self._vertex_count)
        gl.glBindVertexArray(0)
