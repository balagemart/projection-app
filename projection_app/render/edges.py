import numpy as np
import OpenGL.GL as gl
from render.mesh import Mesh


def build_edge_vetors(
    vertices,
    indices,
    components_per_vertex,
    length=1.0
) -> Mesh:

    # flat vertex tömb -> (vertex_count, components_per_vertex)
    verts2d = np.asarray(vertices, dtype=np.float32).reshape(-1, components_per_vertex)

    # positions
    positions = verts2d[:, :3]

    # indexek hármasával -> (triangle_count, 3)
    triangles = np.asarray(indices, dtype=np.uint32).reshape(-1, 3)

    # minden háromszög 3 csúcsa
    p0 = positions[triangles[:, 0]]
    p1 = positions[triangles[:, 1]]
    p2 = positions[triangles[:, 2]]

    # élek
    e1 = p1 - p0
    e2 = p2 - p0
    e3 = p2 - p1

    line_count = positions.shape[0] // 2
    out = np.zeros((line_count, 6), dtype=np.float32)

    out = np.asarray([p0, p1, p0, p2, p1, p2], dtype=np.float32)
    # start pontok
    # out[0::2, 0:3] = positions[0::2]
    # out[0::2, 3:6] = [0.0, 0.0, 1.0]
    #
    # # end pontok
    # out[1::2, 0:3] = positions[0::1]
    # out[1::2, 3:6] = [0.0, 0.0, 1.0]

    return Mesh(
        vertices=out.reshape(-1),
        components_per_vertex=6,
        primitive=gl.GL_LINES
    )
