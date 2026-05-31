import unittest

import numpy as np

from core.camera import ProjectionMode, SceneCamera
from scene.scene import Scene
from scene.transform import Transform


class SceneCameraTests(unittest.TestCase):
    def test_builds_view_and_perspective_projection_matrices(self):
        camera = SceneCamera(transform=Transform())

        self.assertEqual(camera.view_matrix().shape, (4, 4))
        self.assertEqual(camera.projection_matrix(16 / 9).shape, (4, 4))

    def test_builds_orthographic_projection_matrix(self):
        camera = SceneCamera(
            transform=Transform(),
            projection_mode=ProjectionMode.ORTHOGRAPHIC,
        )

        self.assertEqual(camera.projection_matrix(16 / 9).shape, (4, 4))

    def test_scene_object_and_camera_share_transform(self):
        scene = Scene()

        camera_object = scene.get_object(scene.add_camera())

        self.assertIsNotNone(camera_object)
        self.assertIsNotNone(camera_object.camera)
        self.assertIs(camera_object.transform, camera_object.camera.transform)

    def test_view_matrix_changes_when_shared_transform_moves(self):
        transform = Transform()
        camera = SceneCamera(transform=transform)
        initial_view = camera.view_matrix()

        transform.position[0] = 3.0

        self.assertFalse(np.array_equal(initial_view, camera.view_matrix()))


if __name__ == "__main__":
    unittest.main()
