import numpy as np


def camera_wireframe(
    scale: float = 1.0,
    color: tuple[float, float, float] = (1.0, 1.0, 0.0)
):
    s = scale
    r, g, b = color

    vertices = np.array([
        # tip
        0, 0, -1*s, r, g, b,

        # base
        -0.5*s, -0.5*s, 0, r, g, b,
        0.5*s, -0.5*s, 0, r, g, b,
        0.5*s,  0.5*s, 0, r, g, b,
        -0.5*s,  0.5*s, 0, r, g, b,
    ], dtype=np.float32)

    indices = np.array([
        # lines (GL_LINES)
        0, 1,
        0, 2,
        0, 3,
        0, 4,

        1, 2,
        2, 3,
        3, 4,
        4, 1,
    ], dtype=np.uint32)

    return vertices, indices
