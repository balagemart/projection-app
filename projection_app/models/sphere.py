import numpy as np


def sphere_vertices(radius=1.0, stacks=20, slices=20, color=(0.2, 0.6, 1.0)):
    vertices = []
    indices = []
    
    r_col, g_col, b_col = color

    for i in range(stacks + 1):
        theta = np.pi * i / stacks
        sin_t = np.sin(theta)
        cos_t = np.cos(theta)

        for j in range(slices + 1):
            phi = 2 * np.pi * j / slices
            sin_p = np.sin(phi)
            cos_p = np.cos(phi)

            x = radius * sin_t * cos_p
            y = radius * cos_t
            z = radius * sin_p * sin_t

            vertices.extend([x, y, z, r_col, g_col, b_col])
    # index generalas
    for i in range(stacks):
        for j in range(slices):
            first = i * (slices + 1) + j
            second = first + slices + 1

            indices.extend([
                first, second, first + 1,
                second, second + 1, first + 1
            ])

    return (
        np.array(vertices, dtype=np.float32),
        np.array(indices, dtype=np.uint32)
    )
