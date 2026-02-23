import numpy as np


def triangle_vertices() -> np.ndarray:
    return np.array([
         -1.0, -1.0, 0.0,
         1.0, -1.0, 0.0,
         0.0,  1.0, 0.0,
    ], dtype=np.float32)
