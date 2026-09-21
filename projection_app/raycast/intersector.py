import numpy as np

from core.camera import Camera
from raycast.intersections import intersect
from scene.factories import create_pointcloud
from core.camera import ProjectionMode

from raycast.ray_generation import make_ortho_camera_rays, make_perspective_camera_directions


class Intersector():
    def __init__(self, scene):
        self.scene = scene

    def make_intersection(self, cam: Camera) -> None:
        if cam.projection_mode == ProjectionMode.PERSPECTIVE:
            self.make_perspective_intersections(cam)
        elif cam.projection_mode == ProjectionMode.ORTHOGRAPHIC:
            self.make_ortho_intersections(cam)

    def make_ortho_intersections(self, cam: Camera) -> None:
        rays = make_ortho_camera_rays(cam, 128, 72)

        objects_made_of_triangles = []
        for obj in self.scene.objects:
            if obj.made_of_triangles:
                objects_made_of_triangles.append(obj)

        hits_to_make = []
        for ray in rays:
            origin, direction = ray
            closest_hit = None

            for obj in objects_made_of_triangles:
                mesh = obj.get_mesh()

                vertices = mesh.vertices.reshape(-1, 6)[:, :3]
                indices = mesh.indices.reshape(-1, 3)

                for i0, i1, i2 in indices:
                    v0, v1, v2 = vertices[i0], vertices[i1], vertices[i2]

                    hit = intersect(origin, direction, v0, v1, v2)
                    if hit is None:
                        continue

                    if closest_hit is None or hit.t < closest_hit.t:
                        closest_hit = hit

            if closest_hit is not None:
                hits_to_make.append(closest_hit)

        points = np.array([hit.Point for hit in hits_to_make], dtype=np.float32)
        self.scene.add_object(create_pointcloud(points))

    def make_perspective_intersections(self, cam: Camera) -> None:
        directions = make_perspective_camera_directions(cam, 128, 72)

        objects_made_of_triangles = []
        for obj in self.scene.objects:
            if obj.made_of_triangles:
                objects_made_of_triangles.append(obj)

        hits_to_make = []
        for direction in directions:
            closest_hit = None

            for obj in objects_made_of_triangles:
                mesh = obj.get_mesh()

                vertices = mesh.vertices.reshape(-1, 6)[:, :3]
                indices = mesh.indices.reshape(-1, 3)

                for i0, i1, i2 in indices:
                    v0, v1, v2 = vertices[i0], vertices[i1], vertices[i2]

                    hit = intersect(cam.transform.position.copy(), direction, v0, v1, v2)
                    if hit is None:
                        continue

                    if closest_hit is None or hit.t < closest_hit.t:
                        closest_hit = hit

            if closest_hit is not None:
                hits_to_make.append(closest_hit)

        points = np.array([hit.Point for hit in hits_to_make], dtype=np.float32)
        self.scene.add_object(create_pointcloud(points))
