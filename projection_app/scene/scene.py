from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np
from typing import Any

from core.camera import OrbitCamera
from models.cube import cube_vertices_per_vertex_colors, cube_indices
from models.sphere import sphere_vertices


@dataclass
class MeshData:
    """
    CPU-oldali geometry csomag (nem OpenGL):
    - vertices: flat float32 array (pl. xyz vagy xyzrgb)
    - indices: optional uint32 array (EBO-hoz)
    - components_per_vertex: 3 vagy 6
    """
    vertices: np.ndarray          # (N,3) float32, vagy flat is ok
    indices: np.ndarray | None = None  # (M,) uint32
    components_per_vertex: int = 3


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
    type: str
    params: dict[str, Any]
    visible: bool = True
    dirty: bool = True
    mesh_cache: MeshData | None = None

    def generate_mesh(self) -> MeshData:
        """
        Paraméterekből mesh generálás. (CPU)
        """
        type = self.type
        if type == "cube":
            size = self.params["size"]
            verts = cube_vertices_per_vertex_colors(size)
            inds = cube_indices()

            mesh = MeshData(
                vertices=verts,
                indices=inds,
                components_per_vertex=6
            )
        elif type == "sphere":
            radius = self.params["radius"]
            stacks = self.params.get("stacks", 100)
            slices = self.params.get("slices", 100)

            verts, inds = sphere_vertices(radius, stacks, slices)

            mesh = MeshData(
                vertices=verts,
                indices=inds,
                components_per_vertex=6
            )
        elif type == "imported":
            mesh = MeshData(
                vertices=self.params["vertices"],
                indices=self.params["indices"],
                components_per_vertex=self.params["components_per_vertex"]
            )
        else:
            raise ValueError(f"Unknown object type: {self.type}")

        return mesh

    def get_mesh(self) -> MeshData:
        """
        Cache-elt mesh visszaadása.
        Ha dirty vagy nincs cache -> generate_mesh() és cache update.
        """
        if self.dirty or self.mesh_cache is None:
            self.mesh_cache = self.generate_mesh()
            self.dirty = False

        return self.mesh_cache


@dataclass
class Scene:
    camera: OrbitCamera = field(default_factory=OrbitCamera)
    objects: list[SceneObject] = field(default_factory=list)
    selected_id: int | None = None
    _next_id: int = 1

    def add_object(self, obj: SceneObject) -> int:
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
            obj.name = self._default_name_for_type(obj.type)

        self.objects.append(obj)
        return obj.id

    def remove_object(self, obj_id: int) -> bool:
        """
        Objektum törlése id alapján.
        True ha talált és törölt, False ha nem volt ilyen.
        """
        for i, o in enumerate(self.objects):
            if o.id == obj_id:
                self.objects.pop(i)
                if self.selected_id == obj_id:
                    self.selected_id = None
                return True
        return False

    def get_object(self, obj_id: int) -> SceneObject | None:
        for o in self.objects:
            if o.id == obj_id:
                return o
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

    def _default_name_for_type(self, obj_type: str) -> str:
        base = obj_type.capitalize()
        n = sum(1 for o in self.objects if o.type == obj_type) + 1
        return f"{base}{n}"

    def add_cube(self, size: float = 3.0, name: str = "") -> int:
        obj = SceneObject(
            id=0,
            name=name,
            type="cube",
            params={"size": float(size)}
        )
        obj_id = self.add_object(obj)
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
            type="sphere",
            params={
                "radius": float(radius),
                "stacks": int(stacks),
                "slices": int(slices),
            },
        )
        obj_id = self.add_object(obj)
        self.selected_id = obj_id
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
            type="imported",
            params={
                "vertices": vertices,
                "indices": indices,
                "components_per_vertex": int(components_per_vertex),
            },
        )
        obj_id = self.add_object(obj)
        self.select(obj_id)
        return obj_id
