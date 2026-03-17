from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
from typing import Any
from enum import Enum

from core.camera import OrbitCamera, CameraData
from core.transforms import model_matrix
from models.cube import cube_vertices_per_vertex_colors, cube_indices
from models.sphere import sphere_vertices
from models.camera import camera_wireframe


class ObjectType(Enum):
    CUBE = "cube"
    SPHERE = "sphere"
    IMPORTED = "imported"
    CAMERA = "camera"


class PrimitiveType(Enum):
    TRIANGLES = "triangles"
    LINES = "lines"


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


@dataclass
class SceneObject:
    """
    Scene-ben tárolt objektum.
    - params: típusfüggő paraméterek (radius, center, size, stb.)
    - mesh_cache: paraméterből generált MeshData (cache)
    - dirty: ha True -> újra kell generálni a mesh_cache-t
    """
    id: int
    name: str
    obj_type: ObjectType
    params: dict[str, Any]

    position: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    rotation: list[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])  # radians
    scale: list[float] = field(default_factory=lambda: [1.0, 1.0, 1.0])

    visible: bool = True
    show_normals: bool = False

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
        M = model_matrix(self.position, self.rotation, self.scale)
        if self.geometry_dirty or self.local_mesh_cache is None:
            self.local_mesh_cache = self._generate_mesh()
            self.world_mesh_cache = self._apply_transform(self.local_mesh_cache, M)
            self.geometry_dirty = False
            self.transform_dirty = False
        elif self.transform_dirty or self.world_mesh_cache is None:
            self.world_mesh_cache = self._apply_transform(self.local_mesh_cache, M)
            self.transform_dirty = False
        return self.world_mesh_cache

    # --- Private helper ---
    def _generate_mesh(self) -> MeshData | None:
        """
        Paraméterekből mesh generálás. (CPU)
        """
        if self.obj_type == ObjectType.CUBE:
            size = self.params["size"]
            verts = cube_vertices_per_vertex_colors(size)
            inds = cube_indices()

            local_mesh = MeshData(
                vertices=verts,
                indices=inds,
                components_per_vertex=6,
                primitive=PrimitiveType.TRIANGLES
            )
        elif self.obj_type == ObjectType.SPHERE:
            radius = self.params["radius"]
            stacks = self.params.get("stacks", 100)
            slices = self.params.get("slices", 100)

            verts, inds = sphere_vertices(radius, stacks, slices)

            local_mesh = MeshData(
                vertices=verts,
                indices=inds,
                components_per_vertex=6,
                primitive=PrimitiveType.TRIANGLES
            )
        elif self.obj_type == ObjectType.IMPORTED:
            local_mesh = MeshData(
                vertices=self.params["vertices"],
                indices=self.params["indices"],
                components_per_vertex=self.params["components_per_vertex"],
                primitive=PrimitiveType.TRIANGLES
            )
        elif self.obj_type == ObjectType.CAMERA:
            scale = self.params.get("icon_scale", 1.0)
            verts, inds = camera_wireframe(scale)
            local_mesh = MeshData(
                vertices=verts,
                indices=inds,
                components_per_vertex=6,
                primitive=PrimitiveType.LINES
            )
        else:
            raise ValueError(f"Unknown object type: {self.obj_type}")

        return local_mesh

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


@dataclass
class Scene:
    editor_camera: OrbitCamera = field(default_factory=OrbitCamera)
    objects: list[SceneObject] = field(default_factory=list)
    selected_id: int | None = None
    _next_id: int = 1

    # --- Public API ---
    def remove_object(self, obj_id: int) -> bool:
        """
        Objektum törlése id alapján.
        True ha talált és törölt, False ha nem volt ilyen.
        """
        for ind, obj in enumerate(self.objects):
            if obj.id == obj_id:
                self.objects.pop(ind)
                if self.selected_id == obj_id:
                    self.selected_id = None
                return True
        return False

    def get_object(self, obj_id: int) -> SceneObject | None:
        for obj in self.objects:
            if obj.id == obj_id:
                return obj
        return None

    def clear(self) -> None:
        self.objects.clear()
        self.selected_id = None
        self._next_id = 1

    def select(self, obj_id: int | None) -> None:
        """
        Kijelölés állítása.
        - None: kijelölés törlése
        - id: ha létezik -> selected_id beáll
        """
        if obj_id is None:
            self.selected_id = None
            return
        if self.get_object(obj_id) is not None:
            self.selected_id = obj_id
        else:
            self.selected_id = None

    def get_selected_camera(self) -> SceneObject | None:
        for obj in self.objects:
            if (obj.obj_type == ObjectType.CAMERA) and (obj.id == self.selected_id):
                return obj
        return None

    def add_camera(self, name: str = "") -> int:
        cam_data = CameraData()
        obj = SceneObject(
            id=0,
            name=name,
            obj_type=ObjectType.CAMERA,
            params={
                "projection_mode": cam_data.projection_mode,
                "fov_y": cam_data.fov_y,
                "ortho_scale": cam_data.ortho_scale,
                "near": cam_data.near,
                "far": cam_data.far
                }
        )
        obj_id = self._add_object(obj)
        self.select(obj_id)
        return obj_id

    def add_cube(self, size: float = 3.0, name: str = "") -> int:
        obj = SceneObject(
            id=0,
            name=name,
            obj_type=ObjectType.CUBE,
            params={"size": float(size)}
        )
        obj_id = self._add_object(obj)
        self.select(obj_id)
        return obj_id

    def add_sphere(
        self,
        radius: float = 2.0,
        *,
        stacks: int = 100,
        slices: int = 100,
        name: str = "",
    ) -> int:
        obj = SceneObject(
            id=0,
            name=name,
            obj_type=ObjectType.SPHERE,
            params={
                "radius": float(radius),
                "stacks": int(stacks),
                "slices": int(slices),
            }
        )
        obj_id = self._add_object(obj)
        self.select(obj_id)
        return obj_id

    def add_imported(
        self,
        vertices: np.ndarray,
        indices: np.ndarray | None,
        *,
        components_per_vertex: int = 3,
        name: str = "",
    ) -> int:
        obj = SceneObject(
            id=0,
            name=name,
            obj_type=ObjectType.IMPORTED,
            params={
                "vertices": vertices,
                "indices": indices,
                "components_per_vertex": int(components_per_vertex),
            },
        )
        obj_id = self._add_object(obj)
        self.select(obj_id)
        return obj_id

    # --- Private helper ---
    def _default_name_for_type(self, obj_type: ObjectType) -> str:
        base = obj_type.value.capitalize()
        n = sum(1 for o in self.objects if o.obj_type == obj_type) + 1
        return f"{base}{n}"

    def _add_object(self, obj: SceneObject) -> int:
        """
        Objektum hozzáadása a Scene-hez.
        Ha obj.id <= 0, akkor itt kap új id-t.
        Ha név üres, generálunk.
        Visszaadja az objektum id-ját.
        """
        if obj.id <= 0:
            obj.id = self._next_id
            self._next_id += 1
        else:
            self._next_id = max(self._next_id, obj.id + 1)

        if not obj.name:
            obj.name = self._default_name_for_type(obj.obj_type)

        self.objects.append(obj)
        return obj.id
