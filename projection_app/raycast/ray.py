import numpy as np
from dataclasses import dataclass


# Jelenleg nincs hasznalatban ez az osztaly kell egyaltalan ilyen?? scak plussz peldanyositas valszeg
@dataclass
class Ray:
    origin: np.ndarray
    direction: np.ndarray

    def at(self, t: int) -> np.ndarray:
        return self.origin + self.direction * t


@dataclass
class Hit:
    hit: bool
    t: float
    u: float
    v: float
    Point: np.ndarray
