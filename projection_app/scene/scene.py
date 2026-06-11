from __future__ import annotations
from dataclasses import dataclass, field

from core.camera import OrbitCamera
from scene.entity import ObjectType, SceneObject


@dataclass
class Scene:
    editor_camera: OrbitCamera = field(default_factory=OrbitCamera)
    objects: list[SceneObject] = field(default_factory=list)
    selected_id: int | None = None
    _next_id: int = 1

    # --- Public API ---
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
            obj.name = self._default_name_for_type(obj.obj_type)

        self.objects.append(obj)
        self.select(obj.id)

        return obj.id

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

    # --- Private helper ---
    def _default_name_for_type(self, obj_type: ObjectType) -> str:
        base = obj_type.value.capitalize()
        n = sum(1 for o in self.objects if o.obj_type == obj_type) + 1
        return f"{base}{n}"
