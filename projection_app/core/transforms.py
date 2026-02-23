import numpy as np


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


def identity() -> np.ndarray:
    """4x4 egységmátrix."""
    return np.eye(4, dtype=np.float32)
