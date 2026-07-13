import numpy as np


def frustum_wireframe(
    position: np.ndarray,
    forward: np.ndarray,
    right: np.ndarray,
    up: np.ndarray,
    fov_y: float,
    aspect: float,
    near: float,
    far: float,
):
    near_h = 2 * np.tan(fov_y / 2) * near
    near_w = near_h * aspect

    far_h = 2 * np.tan(fov_y / 2) * far
    far_w = far_h * aspect

    near_center = position + forward * near
    far_center = position + forward * far

    ntl = near_center + up * near_h/2 - right * near_w/2
    ntr = near_center + up * near_h/2 + right * near_w/2
    nbl = near_center - up * near_h/2 - right * near_w/2
    nbr = near_center - up * near_h/2 + right * near_w/2

    ftl = far_center + up * far_h/2 - right * far_w/2
    ftr = far_center + up * far_h/2 + right * far_w/2
    fbl = far_center - up * far_h/2 - right * far_w/2
    fbr = far_center - up * far_h/2 + right * far_w/2

    color = np.array([1.0, 1.0, 0.0], dtype=np.float32)
    corners = [ntl, ntr, nbr, nbl, ftl, ftr, fbr, fbl]

    verts = []
    for corner in corners:
        verts.extend([
            corner[0],
            corner[1],
            corner[2],
            color[0],
            color[1],
            color[2],
        ])

    inds = np.array([
        0, 1, 1, 2, 2, 3, 3, 0,
        4, 5, 5, 6, 6, 7, 7, 4,
        0, 4, 1, 5, 2, 6, 3, 7,
    ], dtype=np.uint32)

    return np.array(verts, dtype=np.float32), inds
