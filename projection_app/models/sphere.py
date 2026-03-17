import numpy as np


def sphere_vertices(
    radius: float = 1.0,
    stacks: int = 20,
    slices: int = 20,
    color: tuple[float, float, float] = (0.2, 0.6, 1.0),
) -> tuple[np.ndarray, np.ndarray]:
    stacks = max(2, int(stacks))
    slices = max(3, int(slices))

    r_col, g_col, b_col = color

    theta = np.linspace(0.0, np.pi, stacks + 1, dtype=np.float32)
    phi = np.linspace(0.0, 2.0 * np.pi, slices + 1, dtype=np.float32)

    theta_grid, phi_grid = np.meshgrid(theta, phi, indexing="ij")

    sin_t = np.sin(theta_grid)
    cos_t = np.cos(theta_grid)
    sin_p = np.sin(phi_grid)
    cos_p = np.cos(phi_grid)

    x = radius * sin_t * cos_p
    y = radius * cos_t
    z = radius * sin_t * sin_p

    positions = np.stack((x, y, z), axis=-1)  # (stacks+1, slices+1, 3)

    colors = np.empty_like(positions, dtype=np.float32)
    colors[..., 0] = r_col
    colors[..., 1] = g_col
    colors[..., 2] = b_col

    vertices = np.concatenate((positions, colors), axis=-1).reshape(-1).astype(np.float32)

    row_starts = np.arange(stacks, dtype=np.uint32)[:, None] * (slices + 1)
    col_offsets = np.arange(slices, dtype=np.uint32)[None, :]

    first = row_starts + col_offsets
    second = first + (slices + 1)

    tri1 = np.stack((first, first + 1, second), axis=-1)
    tri2 = np.stack((second, first + 1, second + 1), axis=-1)

    indices = np.concatenate((tri1, tri2), axis=-1).reshape(-1).astype(np.uint32)

    return vertices, indices
