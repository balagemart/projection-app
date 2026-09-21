import unittest

import numpy as np

from geometry.mesh_data import PrimitiveType
from geometry.sources import (
    CameraGeometry,
    CubeGeometry,
    ImportedGeometry,
    SphereGeometry,
)


class GeometrySourceTests(unittest.TestCase):
    def test_cube_geometry_builds_triangle_mesh(self):
        mesh = CubeGeometry(size=2.0).build_mesh()

        self.assertEqual(mesh.primitive, PrimitiveType.TRIANGLES)
        self.assertEqual(mesh.vertices.shape, (8 * 6,))
        self.assertEqual(mesh.indices.shape, (12 * 3,))

    def test_sphere_geometry_uses_requested_resolution(self):
        mesh = SphereGeometry(radius=2.0, stacks=4, slices=6).build_mesh()

        self.assertEqual(mesh.vertices.shape, ((4 + 1) * (6 + 1) * 6,))
        self.assertEqual(mesh.indices.shape, (4 * 6 * 2 * 3,))

    def test_imported_geometry_returns_passed_mesh_data(self):
        vertices = np.array([[0.0, 0.0, 0.0]], dtype=np.float32)
        indices = np.array([0], dtype=np.uint32)

        mesh = ImportedGeometry(vertices, indices).build_mesh()

        self.assertIs(mesh.vertices, vertices)
        self.assertIs(mesh.indices, indices)

    def test_camera_geometry_builds_line_mesh(self):
        mesh = CameraGeometry(size=2.0).build_mesh()

        self.assertEqual(mesh.primitive, PrimitiveType.LINES)
        self.assertEqual(mesh.vertices.shape, (5 * 6,))
        self.assertEqual(mesh.indices.shape, (8 * 2,))


if __name__ == "__main__":
    unittest.main()
