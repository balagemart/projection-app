# import numpy as mp
#
# def cube_vertices(size: float = 1.0) -> np.ndarray:
#     s = size / 2.0
#     return np.array([
#
#     ], dtype=np.float32)

import numpy as np


def cube_vertices_per_vertex_colors(size: float = 1.0) -> np.ndarray:
    """
    8 sarokpont, mindegyiknek más szín (vertex-color demo).
    Vertex formátum: x y z r g b (6 float / vertex)
    """
    s = float(size) / 2.0

    # 8 corners + 8 colors (tetszés szerint)
    corners = [
        (-s, -s, -s),   # 0
        (s, -s, -s),    # 1
        (s, -s,  s),    # 2
        (-s, -s,  s),   # 3
        (-s,  s, -s),   # 4
        (s,  s, -s),    # 5
        (s,  s,  s),    # 6
        (-s,  s,  s),   # 7
    ]
    colors = [
        (1, 0, 0),  # 0 red
        (0, 1, 0),  # 1 green
        (0, 0, 1),  # 2 blue
        (1, 1, 0),  # 3 yellow
        (1, 0, 1),  # 4 magenta
        (0, 1, 1),  # 5 cyan
        (1, 1, 1),  # 6 white
        (0.3, 0.3, 0.3),  # 7 gray
    ]

    data = []
    for (x, y, z), (r, g, b) in zip(corners, colors):
        data += [x, y, z, r, g, b]

    return np.array(data, dtype=np.float32)


def cube_indices() -> np.ndarray:
    """
    12 háromszög -> 36 index.
    Fontos: 8 vertexből dolgozunk, ezért a face-normál/szín nem lesz külön laponként.
    """
    return np.array([
        # bottom (0,1,2,3)
        0, 1, 2,
        0, 2, 3,

        # top (4,5,6,7)
        4, 6, 5,
        4, 7, 6,

        # front (3,2,6,7)  z=+s
        3, 2, 6,
        3, 6, 7,

        # back (0,5,1,4)   z=-s
        0, 5, 4,
        0, 1, 5,

        # left (0,3,7,4)   x=-s
        0, 3, 7,
        0, 7, 4,

        # right (1,6,2,5)  x=+s
        1, 6, 5,
        1, 2, 6,
    ], dtype=np.uint32)
