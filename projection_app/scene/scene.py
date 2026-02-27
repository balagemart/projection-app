from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

from core.camera import OrbitCamera


@dataclass
class SceneMesh:
    # csak adat, semmi OpenGL
    vertices: np.ndarray          # (N,3) float32, vagy flat is ok
    indices: np.ndarray | None = None  # (M,) uint32
    components_per_vertex: int = 3


@dataclass
class Scene:
    camera: OrbitCamera = field(default_factory=OrbitCamera)
    meshes: list[SceneMesh] = field(default_factory=list)

    def clear_meshes(self) -> None:
        self.meshes.clear()

    def add_mesh(
            self,
            vertices: np.ndarray,
            indices: np.ndarray | None = None,
            components_per_vertex: int = 3
            ) -> None:
        self.meshes.append(SceneMesh(
            vertices=vertices,
            indices=indices,
            components_per_vertex=components_per_vertex
            ))
