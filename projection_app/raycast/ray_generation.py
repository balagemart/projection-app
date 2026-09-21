import numpy as np


def make_perspective_camera_directions(cam, x_count: int, y_count: int):
    forward, right, up = cam.basis_vectors()

    aspect = cam.aspect
    fov_y = np.deg2rad(cam.fov_y_deg)

    half_h = np.tan(fov_y / 2.0)
    half_w = half_h * aspect

    directions = []

    for y in range(y_count):
        v = 1.0 - 2.0 * ((y + 0.5) / y_count)  # +1 fent, -1 lent

        for x in range(x_count):
            u = 2.0 * ((x + 0.5) / x_count) - 1.0  # -1 bal, +1 jobb

            direction = (
                forward
                + right * (u * half_w)
                + up * (v * half_h)
            )

            direction = direction / np.linalg.norm(direction)
            directions.append(direction)

    return directions


def make_ortho_camera_rays(cam, x_count: int, y_count: int):
    position = cam.transform.position.copy()
    forward, right, up = cam.basis_vectors()

    half_h = cam.ortho_scale
    half_w = half_h * cam.aspect

    rays = []

    for y in range(y_count):
        v = 1.0 - 2.0 * ((y + 0.5) / y_count)

        for x in range(x_count):
            u = 2.0 * ((x + 0.5) / x_count) - 1.0

            origin = (
                position
                + right * (u * half_w)
                + up * (v * half_h)
            )

            direction = forward

            rays.append((origin, direction))

    return rays
