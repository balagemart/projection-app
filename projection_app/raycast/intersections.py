import numpy as np

from raycast.ray import Hit


def intersect(
        origin,
        direction,
        v0, v1, v2
) -> Hit:
    """
    Möller-Trumbone
    """
    EPSILON = 1e-8
    v0v1 = v1 - v0
    v0v2 = v2 - v0

    pvec = np.cross(direction, v0v2)
    det = np.dot(v0v1, pvec)

    if det < EPSILON:
        return None

    invDet = 1/det

    tvec = origin - v0
    u = np.dot(tvec, pvec) * invDet
    if u < 0 or u > 1:
        return None

    qvec = np.cross(tvec, v0v1)
    v = np.dot(direction, qvec) * invDet
    if v < 0 or u + v > 1:
        return None

    t = np.dot(v0v2, qvec) * invDet
    if t < EPSILON:
        return None

    P = origin + direction * t

    return Hit(True, t, u, v, P)
