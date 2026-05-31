import unittest

import numpy as np

from geometry.sources import CubeGeometry, ImportedGeometry, SphereGeometry
from scene.factories import (
    create_camera,
    create_cube,
    create_imported_mesh,
    create_sphere,
)
from scene.scene import Scene


class FactoryTests(unittest.TestCase):
    def test_create_cube_passes_name_and_size(self):
        obj = create_cube(size=7.0, name="Large cube")

        self.assertEqual(obj.name, "Large cube")
        self.assertIsInstance(obj.geometry, CubeGeometry)
        self.assertEqual(obj.geometry.size, 7.0)

    def test_create_sphere_passes_geometry_settings(self):
        obj = create_sphere(radius=4.0, stacks=8, slices=12)

        self.assertIsInstance(obj.geometry, SphereGeometry)
        self.assertEqual(obj.geometry.radius, 4.0)
        self.assertEqual(obj.geometry.stacks, 8)
        self.assertEqual(obj.geometry.slices, 12)

    def test_create_camera_shares_transform_with_component(self):
        obj = create_camera()

        self.assertIsNotNone(obj.camera)
        self.assertIs(obj.transform, obj.camera.transform)

    def test_create_imported_mesh_preserves_buffers(self):
        vertices = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)
        indices = np.array([0], dtype=np.uint32)

        obj = create_imported_mesh(vertices, indices)

        self.assertIsInstance(obj.geometry, ImportedGeometry)
        self.assertIs(obj.geometry.vertices, vertices)
        self.assertIs(obj.geometry.indices, indices)


class SceneFactoryIntegrationTests(unittest.TestCase):
    def test_add_methods_forward_arguments_and_select_new_object(self):
        scene = Scene()
        obj_id = scene.add_sphere(radius=5.0, stacks=6, slices=9, name="Custom sphere")

        obj = scene.get_object(obj_id)

        self.assertEqual(scene.selected_id, obj_id)
        self.assertEqual(obj.name, "Custom sphere")
        self.assertEqual(obj.geometry.radius, 5.0)
        self.assertEqual(obj.geometry.stacks, 6)
        self.assertEqual(obj.geometry.slices, 9)


if __name__ == "__main__":
    unittest.main()
