from dataclasses import dataclass, field
import numpy as np
from core.transforms import model_matrix


@dataclass
class Transform:
    position: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 0.0, 0.0], dtype=np.float32)
    )
    rotation: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 0.0, 0.0], dtype=np.float32)
    )  # radians
    scale: np.ndarray = field(
        default_factory=lambda: np.array([1.0, 1.0, 1.0], dtype=np.float32)
    )

    def matrix(self) -> np.ndarray:
        return model_matrix(self.position, self.rotation, self.scale)
