from __future__ import annotations
from dataclasses import dataclass, field
import numpy as np

from core.camera import OrbitCamera
from scene.entity import ObjectType, SceneObject
from scene.factories import create_camera, create_cube, create_sphere, create_imported_mesh


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
        obj = create_camera(name=name)
        return self._add_and_select_object(obj)

    def add_cube(self, size: float = 3.0, name: str = "") -> int:
        obj = create_cube(size=size, name=name)
        return self._add_and_select_object(obj)

    def add_sphere(
        self,
        radius: float = 2.0,
        *,
        stacks: int = 100,
        slices: int = 100,
        name: str = "",
    ) -> int:
        obj = create_sphere(
            radius=radius,
            stacks=stacks,
            slices=slices,
            name=name,
        )
        return self._add_and_select_object(obj)

    def add_imported(
        self,
        vertices: np.ndarray,
        indices: np.ndarray | None,
        *,
        components_per_vertex: int = 3,
        name: str = "",
    ) -> int:
        obj = create_imported_mesh(
            vertices=vertices,
            indices=indices,
            components_per_vertex=components_per_vertex,
            name=name,
        )
        return self._add_and_select_object(obj)

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

    def _add_and_select_object(self, obj: SceneObject) -> int:
        obj_id = self._add_object(obj)
        self.select(obj_id)
        return obj_id
