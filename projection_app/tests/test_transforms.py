import unittest

import numpy as np

from core.transforms import (
    identity,
    model_matrix,
    orthographic,
    perspective,
    rotation_matrix_z,
    scale_matrix,
    translation_matrix,
)


class TransformTests(unittest.TestCase):
    def test_identity_matrix(self):
        np.testing.assert_array_equal(identity(), np.eye(4, dtype=np.float32))

    def test_translation_matrix_moves_homogeneous_point(self):
        matrix = translation_matrix(np.array([2.0, -1.0, 3.0]))
        point = np.array([1.0, 2.0, 3.0, 1.0])

        np.testing.assert_allclose(matrix @ point, [3.0, 1.0, 6.0, 1.0])

    def test_scale_matrix_scales_point(self):
        matrix = scale_matrix(np.array([2.0, 3.0, 4.0]))
        point = np.array([1.0, 2.0, 3.0, 1.0])

        np.testing.assert_allclose(matrix @ point, [2.0, 6.0, 12.0, 1.0])

    def test_rotation_matrix_z_rotates_point_counterclockwise(self):
        matrix = rotation_matrix_z(np.pi / 2.0)
        point = np.array([1.0, 0.0, 0.0, 1.0])

        np.testing.assert_allclose(matrix @ point, [0.0, 1.0, 0.0, 1.0], atol=1e-6)

    def test_model_matrix_applies_scale_then_translation(self):
        matrix = model_matrix(
            position=np.array([1.0, 2.0, 3.0]),
            rotation=np.array([0.0, 0.0, 0.0]),
            scale=np.array([2.0, 2.0, 2.0]),
        )
        point = np.array([1.0, 1.0, 1.0, 1.0])

        np.testing.assert_allclose(matrix @ point, [3.0, 4.0, 5.0, 1.0])

    def test_projection_matrices_have_expected_shape(self):
        self.assertEqual(perspective(np.deg2rad(60.0), 16 / 9, 0.1, 100.0).shape, (4, 4))
        self.assertEqual(orthographic(-2.0, 2.0, -1.0, 1.0, 0.1, 100.0).shape, (4, 4))


if __name__ == "__main__":
    unittest.main()
