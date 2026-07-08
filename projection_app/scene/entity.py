from dataclasses import dataclass, field
from enum import Enum
import numpy as np

from geometry.mesh_data import MeshData
from geometry.sources import GeometrySource
from scene.transform import Transform
from scene.links import ObjectLink
from core.camera import SceneCamera


class ObjectType(Enum):
    POINT = "point"
    LINE = "line"
    CUBE = "cube"
    SPHERE = "sphere"
    IMPORTED = "imported"
    CAMERA = "camera"


@dataclass
class SceneObject:
    """
    Scene-ben tárolt objektum.
    - geometry: az objektum CPU-oldali mesh forrása
    - camera: opcionális lehelyezhető kamera komponens
    - mesh_cache: paraméterből generált MeshData (cache)
    - dirty: ha True -> újra kell generálni a mesh_cache-t
    """
    id: int
    name: str
    obj_type: ObjectType

    geometry: GeometrySource | None = None
    camera: SceneCamera | None = None
    link: ObjectLink | None = None

    transform: Transform = field(default_factory=Transform)

    visible: bool = True
    show_normals: bool = False
    show_edges: bool = False
    made_of_triangles: bool = False

    geometry_dirty: bool = True
    transform_dirty: bool = True

    local_mesh_cache: MeshData | None = None
    world_mesh_cache: MeshData | None = None

    # --- Public API ---
    def get_mesh(self) -> MeshData | None:
        """
        Cache-elt mesh visszaadása.
        Ha dirty vagy nincs cache -> generate_mesh() és cache update.
        """
        if self.geometry is None:
            return None
        M = self.transform.matrix()
        if self.geometry_dirty or self.local_mesh_cache is None:
            self.local_mesh_cache = self.geometry.build_mesh()
            self.world_mesh_cache = self._apply_transform(self.local_mesh_cache, M)
            self.geometry_dirty = False
            self.transform_dirty = False
        elif self.transform_dirty or self.world_mesh_cache is None:
            self.world_mesh_cache = self._apply_transform(self.local_mesh_cache, M)
            self.transform_dirty = False
        return self.world_mesh_cache

    # --- Private helpers ---

    def _apply_transform(self, mesh: MeshData, model_matrix: np.ndarray) -> MeshData:
        verts = mesh.vertices.copy()
        c = mesh.components_per_vertex

        # NxC shape
        verts = verts.reshape(-1, c)

        # xyz coords
        positions = verts[:, 0:3]

        # homogenous coords
        ones = np.ones((positions.shape[0], 1), dtype=np.float32)
        positions_h = np.hstack((positions, ones))

        # transform
        positions_transformed = positions_h @ model_matrix.T

        # xyz
        verts[:, 0:3] = positions_transformed[:, 0:3]

        return MeshData(
                vertices=verts.reshape(-1).copy(),
                indices=mesh.indices,
                components_per_vertex=mesh.components_per_vertex,
                primitive=mesh.primitive
        )
