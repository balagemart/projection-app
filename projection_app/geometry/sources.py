from dataclasses import dataclass
from typing import Protocol

import numpy as np

from geometry.mesh_data import MeshData, PrimitiveType
from models.cube import cube_indices, cube_vertices_per_vertex_colors
from models.sphere import sphere_vertices
from models.camera import camera_wireframe


#  TODO EGY HELYEN BEALLITANI A STACKS RADIUS STB ALAP ERTEKET CONSTBA ES NE MAGIC NUMBER LEGYEN
#  VALOSZINULEG ITT ALKALMAS ES AKKOR A SCENEBEN NEM IS KELL OKET MEGADNI

# TODO program elcrashel ha normalst be akarom kapcsolni a kapera wireframere

class GeometrySource(Protocol):
    def build_mesh(self) -> MeshData:
        ...


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
    scale: float = 1.0

    def build_mesh(self) -> MeshData:
        verts, inds = camera_wireframe(self.scale)

        return MeshData(
            vertices=verts,
            indices=inds,
            components_per_vertex=6,
            primitive=PrimitiveType.LINES
        )
