import numpy as np


def identity() -> np.ndarray:
    """4x4 identity matrix."""
    return np.eye(4, dtype=np.float32)


def translation_matrix(position: np.ndarray) -> np.ndarray:
    """4x4 translation matrix."""
    tx, ty, tz = position

    T = np.eye(4, dtype=np.float32)

    T[0, 3] = tx
    T[1, 3] = ty
    T[2, 3] = tz

    return T


def scale_matrix(scale: np.ndarray) -> np.ndarray:
    """4x4 scale matrix."""
    sx, sy, sz = scale

    S = np.eye(4, dtype=np.float32)

    S[0, 0] = sx
    S[1, 1] = sy
    S[2, 2] = sz

    return S


def rotation_matrix_x(angle: float) -> np.ndarray:
    """4x4 rotation matrix on the x axes"""
    c = np.cos(angle)
    s = np.sin(angle)

    Rx = np.eye(4, dtype=np.float32)

    Rx[1, 1] = c
    Rx[1, 2] = -s
    Rx[2, 1] = s
    Rx[2, 2] = c

    return Rx


def rotation_matrix_y(angle: float) -> np.ndarray:
    """4x4 rotation matrix on the y axes"""
    c = np.cos(angle)
    s = np.sin(angle)

    Ry = np.eye(4, dtype=np.float32)

    Ry[0, 0] = c
    Ry[0, 2] = s
    Ry[2, 0] = -s
    Ry[2, 2] = c

    return Ry


def rotation_matrix_z(angle: float) -> np.ndarray:
    """4x4 rotation matrix on the z axes"""
    c = np.cos(angle)
    s = np.sin(angle)

    Rz = np.eye(4, dtype=np.float32)

    Rz[0, 0] = c
    Rz[0, 1] = -s
    Rz[1, 0] = s
    Rz[1, 1] = c

    return Rz


def model_matrix(
        position: np.ndarray,
        rotation: np.ndarray,
        scale: np.ndarray
) -> np.ndarray:
    T = translation_matrix(position)
    S = scale_matrix(scale)

    rx, ry, rz = rotation

    Rx = rotation_matrix_x(rx)
    Ry = rotation_matrix_y(ry)
    Rz = rotation_matrix_z(rz)

    R = Rz @ Ry @ Rx
    M = T @ R @ S

    return M


def look_at(eye: np.ndarray, target: np.ndarray, up: np.ndarray) -> np.ndarray:
    """
    View mátrix számítása klasszikus LookAt formulával.
    eye: kamera pozíció
    target: nézett pont
    up: világ up irány
    """
    f = target - eye
    f = f / np.linalg.norm(f)

    u = up / np.linalg.norm(up)

    s = np.cross(f, u)
    s = s / np.linalg.norm(s)

    u = np.cross(s, f)

    m = np.eye(4, dtype=np.float32)

    m[0, 0:3] = s
    m[1, 0:3] = u
    m[2, 0:3] = -f
    m[0, 3] = -np.dot(s, eye)
    m[1, 3] = -np.dot(u, eye)
    m[2, 3] = np.dot(f, eye)

    return m


def perspective(
        fov_y_rad: float,
        aspect: float,
        near: float,
        far: float
) -> np.ndarray:
    """
    Perspektív vetítési mátrix (jobbkezes rendszer).
    fov_y_rad: vertikális látószög radiánban
    aspect: szélesség / magasság
    near, far: vágósíkok
    """
    f = 1.0 / np.tan(fov_y_rad / 2.0)

    m = np.zeros((4, 4), dtype=np.float32)
    m[0, 0] = f / aspect
    m[1, 1] = f
    m[2, 2] = (far + near) / (near - far)
    m[2, 3] = (2.0 * far * near) / (near - far)
    m[3, 2] = -1.0

    return m


def orthographic(
        left: float,
        right: float,
        bottom: float,
        top: float,
        near: float,
        far
) -> np.ndarray:
    m = np.eye(4, dtype=np.float32)
    m[0, 0] = 2 / (right - left)
    m[1, 1] = 2 / (top - bottom)
    m[2, 2] = -2 / (far - near)

    m[0, 3] = -((right + left) / (right - left))
    m[1, 3] = -((top + bottom) / (top - bottom))
    m[2, 3] = -((far + near) / (far - near))

    return m
