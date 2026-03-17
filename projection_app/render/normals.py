import numpy as np
import OpenGL.GL as gl
from render.mesh import Mesh


def build_face_normals(
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

    # minden háromszög 3 pontja
    p0 = positions[triangles[:, 0]]
    p1 = positions[triangles[:, 1]]
    p2 = positions[triangles[:, 2]]

    # élek
    e1 = p1 - p0
    e2 = p2 - p0

    # face normálok
    normals = np.cross(e1, e2)

    # hosszak
    norm_lengths = np.linalg.norm(normals, axis=1)

    # degenerált háromszögek kiszűrése
    valid = norm_lengths > 1e-8
    if not np.any(valid):
        return Mesh(
            vertices=np.array([], dtype=np.float32),
            components_per_vertex=6,
            primitive=gl.GL_LINES
        )

    p0 = p0[valid]
    p1 = p1[valid]
    p2 = p2[valid]
    normals = normals[valid]
    norm_lengths = norm_lengths[valid]

    # normalizálás
    normals = normals / norm_lengths[:, None]

    # középpontok és végpontok
    centers = (p0 + p1 + p2) / 3.0
    ends = centers + length * normals

    # line vertexek összeállítása: center, end, center, end...
    line_count = centers.shape[0]
    out = np.zeros((line_count * 2, 6), dtype=np.float32)

    # center pontok
    out[0::2, 0:3] = centers
    out[0::2, 3:6] = [1.0, 0.0, 0.0]

    # end pontok
    out[1::2, 0:3] = ends
    out[1::2, 3:6] = [1.0, 0.0, 0.0]

    return Mesh(
        vertices=out.reshape(-1),
        components_per_vertex=6,
        primitive=gl.GL_LINES
    )
