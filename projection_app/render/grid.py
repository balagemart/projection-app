import numpy as np
import OpenGL.GL as gl
from render.mesh import Mesh


def create_grid(size=30, step=1.0, color=(0.55, 0.55, 0.55)) -> Mesh:
    r, g, b = color
    data = []

    for i in range(-size, size + 1):
        # X irányú vonal: (-size,0,i) -> (size,0,i)
        data += [-size*step, 0.0, i*step, r, g, b]
        data += [size*step, 0.0, i*step, r, g, b]

        # Z irányú vonal: (i,0,-size) -> (i,0,size)
        data += [i*step, 0.0, -size*step, r, g, b]
        data += [i*step, 0.0,  size*step, r, g, b]

    vertices = np.array(data, dtype=np.float32)
    return Mesh(
            vertices=vertices,
            components_per_vertex=6,
            primitive=gl.GL_LINES
            )
