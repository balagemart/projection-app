from __future__ import annotations
from enum import Enum

import numpy as np
from dataclasses import dataclass, field
from typing import ClassVar

from core.transforms import perspective, look_at, identity, orthographic


class ProjectionMode(Enum):
    PERSPECTIVE = "perspective"
    ORTHOGRAPHIC = "orthographic"


class ViewMode(Enum):
    FREE = "free"
    FRONT = "front"
    TOP = "top"
    BOTTOM = "bottom"
    RIGHT = "right"
    ISOMETRIC = "isometric"


@dataclass
class CameraData():
    projection_mode: ProjectionMode = ProjectionMode.PERSPECTIVE
    fov_y: float = 60.0
    ortho_scale: float | None = None
    near: float = 0.1
    far: float = 100.0


@dataclass
class OrbitCamera:
    """
    Blender-szerű orbit kamera:
    - target körül kering (yaw/pitch)
    - distance = távolság a targettől (zoom)
    """
    DISTANCE: ClassVar[float] = 12.0
    ORTHO_SCALE: ClassVar[float] = 10.0
    TARGET: ClassVar[np.ndarray] = np.array([0.0, 0.0, 0.0], dtype=np.float32)

    target: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 0.0, 0.0], dtype=np.float32)
    )
    up: np.ndarray = field(
        default_factory=lambda: np.array([0.0, 1.0, 0.0], dtype=np.float32)
    )

    yaw: float = np.deg2rad(45.0)
    pitch: float = np.deg2rad(25.0)
    distance: float = DISTANCE

    fov_y_deg: float = 60.0
    near: float = 0.1
    far: float = 100.0

    projection_mode: ProjectionMode = ProjectionMode.PERSPECTIVE
    view_mode: ViewMode = ViewMode.FREE
    ortho_scale: float = ORTHO_SCALE

    # --- Public camera API ---
    def orbit(self, dx: float, dy: float, sens: float = 0.01) -> None:
        """Jobb egér húzás: orbit."""
        self.yaw += dx * sens
        self.pitch += dy * sens
        self._clamp_pitch()

    def zoom_wheel(
            self,
            wheel_delta_y: int,
            step_in: float = 0.9,
            step_out: float = 1.1
            ) -> None:
        """Görgő: zoom."""
        if self.projection_mode == ProjectionMode.PERSPECTIVE:
            self.distance *= (step_in if wheel_delta_y > 0 else step_out)
            self._clamp_distance()
        elif self.projection_mode == ProjectionMode.ORTHOGRAPHIC:
            self.ortho_scale *= (step_in if wheel_delta_y > 0 else step_out)
            self._clamp_ortho_scale()

    # --- Public view API ---
    def set_front_view(self) -> None:
        self._set_orthographic_view(ViewMode.FRONT, 0.0, 0.0)

    def set_top_view(self) -> None:
        self._set_orthographic_view(ViewMode.TOP, 0.0, np.pi/2-1e-3)

    def set_bottom_view(self) -> None:
        self._set_orthographic_view(ViewMode.BOTTOM, 0.0, -np.pi/2+1e-3)

    def set_right_view(self) -> None:
        self._set_orthographic_view(ViewMode.RIGHT, np.pi/2, 0.0)

    def set_isometric_view(self) -> None:
        self._set_orthographic_view(ViewMode.ISOMETRIC, np.deg2rad(45.0), np.deg2rad(35.264))

    def set_perspective_view(self) -> None:
        self.view_mode = ViewMode.FREE
        self.projection_mode = ProjectionMode.PERSPECTIVE
        self.yaw = np.deg2rad(45.0)
        self.pitch = np.deg2rad(25.0)
        self.distance = self.DISTANCE
        self.target = self.TARGET.copy()

    # --- Public mathematical API ---
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
        eye = self.eye()
        up = self.up

        if self.view_mode == ViewMode.TOP:
            up = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        elif self.view_mode == ViewMode.BOTTOM:
            up = np.array([0.0, 0.0, 1.0], dtype=np.float32)

        return look_at(eye, self.target, up)

    def projection_matrix(self, aspect: float) -> np.ndarray:
        if self.projection_mode == ProjectionMode.PERSPECTIVE:
            return perspective(
                    np.deg2rad(self.fov_y_deg),
                    aspect,
                    self.near,
                    self.far)
        elif self.projection_mode == ProjectionMode.ORTHOGRAPHIC:
            half_h = self.ortho_scale
            half_w = half_h * aspect
            return orthographic(
                        -half_w,
                        half_w,
                        -half_h,
                        half_h,
                        self.near,
                        self.far,)
        raise ValueError(f"Unsupported projection mode: {self.projection_mode}")

    def mvp(
            self,
            aspect: float,
            model: np.ndarray | None = None
    ) -> np.ndarray:
        if model is None:
            model = identity()
        return self.projection_matrix(aspect) @ self.view_matrix() @ model

    # --- Private helpers ---
    def _set_orthographic_view(
            self,
            view_mode: ViewMode,
            yaw: float,
            pitch: float,
    ) -> None:
        self.view_mode = view_mode
        self.projection_mode = ProjectionMode.ORTHOGRAPHIC

        self.yaw = yaw
        self.pitch = pitch
        self.distance = self.DISTANCE
        self.ortho_scale = self.ORTHO_SCALE
        self.target = self.TARGET.copy()

    def _clamp_pitch(self, lo: float = -1.5, hi: float = 1.5) -> None:
        self.pitch = max(lo, min(hi, self.pitch))

    def _clamp_distance(self, lo: float = 0.2, hi: float = 50.0) -> None:
        self.distance = max(lo, min(hi, self.distance))

    def _clamp_ortho_scale(self, lo: float = 0.1, hi: float = 200.0) -> None:
        self.ortho_scale = max(lo, min(hi, self.ortho_scale))
