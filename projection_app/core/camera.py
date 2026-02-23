from __future__ import annotations

import numpy as np
from dataclasses import dataclass, field

from core.transforms import perspective, look_at, identity


@dataclass
class OrbitCamera:
    """
    Blender-szerű orbit kamera:
    - target körül kering (yaw/pitch)
    - distance = távolság a targettől (zoom)
    """
    target: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 0.0, 0.0], dtype=np.float32)
    )
    up: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 1.0, 0.0], dtype=np.float32)
    )

    yaw: float = np.deg2rad(45.0)
    pitch: float = np.deg2rad(25.0)
    distance: float = np.deg2rad(700.0)

    fov_y_deg: float = 60.0
    near: float = 0.1
    far: float = 100.0

    def clamp_pitch(self, lo: float = -1.5, hi: float = 1.5) -> None:
        self.pitch = max(lo, min(hi, self.pitch))

    def clamp_distance(self, lo: float = 0.2, hi: float = 50.0) -> None:
        self.distance = max(lo, min(hi, self.distance))

    def orbit(self, dx: float, dy: float, sens: float = 0.01) -> None:
        """Jobb egér húzás: orbit."""
        self.yaw += dx * sens
        self.pitch += dy * sens
        self.clamp_pitch()

    def zoom_wheel(
            self,
            wheel_delta_y: int,
            step_in: float = 0.9,
            step_out: float = 1.1
            ) -> None:
        """Görgő: zoom."""
        self.distance *= (step_in if wheel_delta_y > 0 else step_out)
        self.clamp_distance()

    def eye(self) -> np.ndarray:
        """Kamera pozíció (eye) kiszámítása yaw/pitch/distance-ból."""
        cy, sy = np.cos(self.yaw), np.sin(self.yaw)
        cp, sp = np.cos(self.pitch), np.sin(self.pitch)

        return self.target + np.array([
            self.distance * cp * sy,
            self.distance * sp,
            self.distance * cp * cy,
        ], dtype=np.float32)

    def view_matrix(self) -> np.ndarray:
        return look_at(self.eye(), self.target, self.up)

    def projection_matrix(self, aspect: float) -> np.ndarray:
        return perspective(
                np.deg2rad(self.fov_y_deg),
                aspect,
                self.near,
                self.far
                )

    def mvp(
            self,
            aspect: float,
            model: np.ndarray | None = None
            ) -> np.ndarray:
        if model is None:
            model = identity()
        return self.projection_matrix(aspect) @ self.view_matrix() @ model
