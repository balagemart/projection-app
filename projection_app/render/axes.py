import numpy as np
import OpenGL.GL as gl
from render.mesh import Mesh


def create_axes(length=30.0) -> Mesh:
    l = length
    eps = 0.001

    # format: kp color vp color
    vertices = np.array([
        0, eps, 0,    1, 0, 0,    l, eps, 0,      1, 0, 0,    # X
        0, eps, 0,    0, 1, 0,    0, eps+l, 0,    0, 1, 0,    # Y
        0, eps, 0,    0, 0, 1,    0, eps, l,      0, 0, 1,    # Z
    ], dtype=np.float32)

    return Mesh(
            vertices=vertices,
            components_per_vertex=6,
            primitive=gl.GL_LINES
            )
