import numpy as np
from enum import Enum
from dataclasses import dataclass


class PrimitiveType(Enum):
    TRIANGLES = "triangles"
    LINES = "lines"
    POINTS = "points"


@dataclass
class MeshData:
    """
    CPU-oldali geometry csomag:
    - vertices: flat float32 array (pl. xyz vagy xyzrgb)
    - indices: optional uint32 array (EBO-hoz)
    - components_per_vertex: 3 vagy 6
    """
    vertices: np.ndarray          # (N,3) float32, vagy flat is ok
    indices: np.ndarray | None = None  # (M,) uint32
    components_per_vertex: int = 3
    primitive: PrimitiveType = PrimitiveType.TRIANGLES
