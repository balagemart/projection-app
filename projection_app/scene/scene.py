from __future__ import annotations
from dataclasses import dataclass, field

from core.camera import OrbitCamera
from scene.entity import ObjectType, SceneObject

from geometry.mesh_data import MeshData
from geometry.sources import LineGeometry

# -- intersection test
from render.ray import Ray, Hit
import numpy as np
from scene.factories import create_point, create_line_between
# -- intersection test


@dataclass
class Scene:
    editor_camera: OrbitCamera = field(default_factory=OrbitCamera)
    objects: list[SceneObject] = field(default_factory=list)
    selected_id: int | None = None
    _next_id: int = 1

# -- intersection test
    def intersect(
            self,
            origin,
            direction,
            v0, v1, v2
    ) -> Hit:
        # compute the normal of the plane
        v0v1 = v1 - v0
        v0v2 = v2 - v0
        N = np.cross(v0v1, v0v2)
        denom = np.dot(N, N)

        NdotRayDir = np.dot(N, direction)
        EPSILON = 1e-8
        if abs(NdotRayDir) < EPSILON:
            return None

        # calculating P
        d = -np.dot(N, v0)
        t = -(np.dot(N, origin) + d) / NdotRayDir

        if t < 0:
            return None

        P = origin + t * direction

        # calculating u
        v1P = P - v1
        v1v2 = v2 - v1
        C = np.cross(v1v2, v1P)
        u = np.dot(N, C)
        if u < 0:
            return None

        # calculating v
        v2P = P - v2
        v2v0 = v0 - v2
        C = np.cross(v2v0, v2P)
        v = np.dot(N, C)
        if v < 0:
            return None

        v0P = P - v0
        C = np.cross(v0v1, v0P)
        if np.dot(N, C) < 0:
            return None

        u /= denom
        v /= denom

        return Hit(True, t, u, v, P)

    def make_intersections_on_cube(self) -> None:
        print("VAN szandek")
        for obj in self.objects:
            if obj.name == "Camera1":
                print("VAN CAM")
                cam = obj
                for obj in self.objects:
                    if obj.name == "Cube1":
                        print("VAN KOCKA")
                        # mesh = obj.get_mesh()
                        mesh = obj.geometry.build_mesh()
                        vertices = mesh.vertices

                        vertices = vertices.reshape(-1, 6)
                        print(vertices.shape)
                        vertices = vertices[:, :3]

                        directions = []
                        ray_count = 36

                        for i in range(ray_count):
                            angle = 2 * np.pi * i / ray_count

                            direction = np.array([
                                np.cos(angle),   # x
                                0.0,             # y
                                np.sin(angle)    # z
                            ], dtype=np.float32)

                            directions.append(direction)

                        directions = []

                        azimuth_count = 36     # körbe, XZ síkban
                        elevation_count = 18   # fel-le

                        for j in range(elevation_count):
                            elevation = -np.pi / 2 + np.pi * j / (elevation_count - 1)

                            for i in range(azimuth_count):
                                azimuth = 2 * np.pi * i / azimuth_count

                                direction = np.array([
                                    np.cos(elevation) * np.cos(azimuth),  # x
                                    np.sin(elevation),                    # y
                                    np.cos(elevation) * np.sin(azimuth),  # z
                                ], dtype=np.float32)

                                direction = direction / np.linalg.norm(direction)
                                directions.append(direction)

                        for i0, i1, i2 in mesh.indices.reshape(-1, 3):
                            v0, v1, v2 = vertices[i0], vertices[i1], vertices[i2]
                            for direction in directions:
                                hit = self.intersect(cam.transform.position, direction, v0, v1, v2)
                                if hit is not None:
                                    print("HIT!")
                                    pointA = create_point()
                                    pointA.transform.position = hit.Point
                                    pointA_id = self.add_object(pointA)

                                    pointB = create_point()
                                    pointB.transform.position = cam.transform.position
                                    pointB_id = self.add_object(pointB)

                                    self.add_object(create_line_between(pointA_id, pointB_id))
                                    self.add_object(create_point())
# -- intersection test

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

    def get_object_mesh(self, obj: SceneObject) -> MeshData | None:
        if obj.obj_type == ObjectType.LINE:
            return self._build_line_mesh(obj)

        return obj.get_mesh()

    def get_selected_camera(self) -> SceneObject | None:
        for obj in self.objects:
            if (obj.obj_type == ObjectType.CAMERA) and (obj.id == self.selected_id):
                return obj
        return None

    # --- Private helper ---
    def _build_line_mesh(self, obj: SceneObject) -> MeshData | None:
        if obj.link is None:
            return None

        start_obj = self.get_object(obj.link.start_id)
        end_obj = self.get_object(obj.link.end_id)

        if start_obj is None or end_obj is None:
            return None

        return LineGeometry(
            start=start_obj.transform.position,
            end=end_obj.transform.position,
        ).build_mesh()

    def _default_name_for_type(self, obj_type: ObjectType) -> str:
        base = obj_type.value.capitalize()
        n = sum(1 for o in self.objects if o.obj_type == obj_type) + 1
        return f"{base}{n}"
