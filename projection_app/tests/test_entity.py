import unittest

import numpy as np

from geometry.sources import CubeGeometry
from scene.entity import ObjectType, SceneObject
from scene.transform import Transform


class TransformTests(unittest.TestCase):
    def test_matrix_uses_position_rotation_and_scale(self):
        transform = Transform(
            position=np.array([1.0, 2.0, 3.0], dtype=np.float32),
            rotation=np.array([0.0, 0.0, 0.0], dtype=np.float32),
            scale=np.array([2.0, 2.0, 2.0], dtype=np.float32),
        )
        point = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)

        np.testing.assert_allclose(transform.matrix() @ point, [3.0, 4.0, 5.0, 1.0])


class SceneObjectTests(unittest.TestCase):
    def test_get_mesh_applies_object_transform(self):
        obj = SceneObject(
            id=1,
            name="Cube",
            obj_type=ObjectType.CUBE,
            geometry=CubeGeometry(size=2.0),
        )
        obj.transform.position[0] = 3.0

        positions = obj.get_mesh().vertices.reshape(-1, 6)[:, :3]

        self.assertEqual(float(np.min(positions[:, 0])), 2.0)
        self.assertEqual(float(np.max(positions[:, 0])), 4.0)


if __name__ == "__main__":
    unittest.main()
