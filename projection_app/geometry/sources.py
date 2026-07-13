from dataclasses import dataclass
from typing import Protocol

import numpy as np

from geometry.mesh_data import MeshData, PrimitiveType
from models.cube import cube_indices, cube_vertices_per_vertex_colors, cube_vertices_single_color
from models.sphere import sphere_vertices
from models.camera import camera_wireframe
from models.frustum import frustum_wireframe
from core.camera import SceneCamera


#  TODO EGY HELYEN BEALLITANI A STACKS RADIUS STB ALAP ERTEKET CONSTBA ES NE MAGIC NUMBER LEGYEN
#  VALOSZINULEG ITT ALKALMAS ES AKKOR A SCENEBEN NEM IS KELL OKET MEGADNI

# TODO program elcrashel ha normalst be akarom kapcsolni a kapera wireframere

class GeometrySource(Protocol):
    def build_mesh(self) -> MeshData:
        ...


@dataclass
class PointGeometry:
    size: float = 0.15
    color: tuple[float, float, float] = (1.0, 0.85, 0.0)

    def build_mesh(self) -> MeshData:
        verts = cube_vertices_single_color(self.size, self.color)
        inds = cube_indices()

        return MeshData(
            vertices=verts,
            indices=inds,
            components_per_vertex=6,
            primitive=PrimitiveType.TRIANGLES
        )


@dataclass
class LineGeometry:
    start: np.ndarray
    end: np.ndarray
    color: tuple[float, float, float] = (1.0, 1.0, 0.0)

    def build_mesh(self) -> MeshData:
        r, g, b = self.color
        verts = np.array([
            self.start[0], self.start[1], self.start[2], r, g, b,
            self.end[0], self.end[1], self.end[2], r, g, b
        ], dtype=np.float32)

        inds = np.array([0, 1], dtype=np.uint32)

        return MeshData(
            vertices=verts,
            indices=inds,
            components_per_vertex=6,
            primitive=PrimitiveType.LINES
        )


@dataclass
class CubeGeometry:
    size: float = 3.0

    def build_mesh(self) -> MeshData:
        verts = cube_vertices_per_vertex_colors(self.size)
        inds = cube_indices()

        return MeshData(
            vertices=verts,
            indices=inds,
            components_per_vertex=6,
            primitive=PrimitiveType.TRIANGLES
        )


@dataclass
class SphereGeometry:
    radius: float = 2.0
    stacks: int = 100
    slices: int = 100

    def build_mesh(self) -> MeshData:
        verts, inds = sphere_vertices(self.radius, self.stacks, self.slices)

        return MeshData(
            vertices=verts,
            indices=inds,
            components_per_vertex=6,
            primitive=PrimitiveType.TRIANGLES
        )


@dataclass
class ImportedGeometry:
    vertices: np.ndarray
    indices: np.ndarray | None
    components_per_vertex: int = 3

    def build_mesh(self) -> MeshData:
        return MeshData(
            vertices=self.vertices,
            indices=self.indices,
            components_per_vertex=self.components_per_vertex,
            primitive=PrimitiveType.TRIANGLES
        )


@dataclass
class CameraGeometry:
    size: float = 1.0

    def build_mesh(self) -> MeshData:
        verts, inds = camera_wireframe(self.size)

        return MeshData(
            vertices=verts,
            indices=inds,
            components_per_vertex=6,
            primitive=PrimitiveType.LINES
        )


@dataclass
class FrustumGeometry:
    position: np.ndarray
    forward: np.ndarray
    right: np.ndarray
    up: np.ndarray
    fov_y: float
    aspect: float
    near: float
    far: float

    def build_mesh(self) -> MeshData:
        verts, inds = frustum_wireframe(
            self.position,
            self.forward,
            self.right,
            self.up,
            self.fov_y,
            self.aspect,
            self.near,
            self.far
        )

        return MeshData(
            vertices=verts,
            indices=inds,
            components_per_vertex=6,
            primitive=PrimitiveType.LINES
        )
