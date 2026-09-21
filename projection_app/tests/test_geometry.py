import unittest

import numpy as np

from models.cube import cube_indices, cube_vertices_per_vertex_colors
from models.sphere import sphere_vertices


class CubeGeometryTests(unittest.TestCase):
    def test_cube_contains_eight_colored_vertices_and_twelve_triangles(self):
        vertices = cube_vertices_per_vertex_colors(size=2.0)
        indices = cube_indices()

        self.assertEqual(vertices.dtype, np.float32)
        self.assertEqual(vertices.shape, (8 * 6,))
        self.assertEqual(indices.dtype, np.uint32)
        self.assertEqual(indices.shape, (12 * 3,))
        self.assertTrue(np.all(np.abs(vertices.reshape(-1, 6)[:, :3]) == 1.0))


class SphereGeometryTests(unittest.TestCase):
    def test_sphere_vertex_and_triangle_count_matches_resolution(self):
        stacks = 4
        slices = 6

        vertices, indices = sphere_vertices(radius=2.0, stacks=stacks, slices=slices)

        self.assertEqual(vertices.dtype, np.float32)
        self.assertEqual(vertices.shape, ((stacks + 1) * (slices + 1) * 6,))
        self.assertEqual(indices.dtype, np.uint32)
        self.assertEqual(indices.shape, (stacks * slices * 2 * 3,))

    def test_sphere_positions_are_on_requested_radius(self):
        vertices, _ = sphere_vertices(radius=2.5, stacks=8, slices=12)
        positions = vertices.reshape(-1, 6)[:, :3]

        np.testing.assert_allclose(
            np.linalg.norm(positions, axis=1),
            2.5,
            rtol=1e-5,
            atol=1e-5,
        )


if __name__ == "__main__":
    unittest.main()
