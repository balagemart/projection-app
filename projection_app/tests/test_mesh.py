import unittest
from unittest.mock import patch

from render.mesh import Mesh


class MeshTests(unittest.TestCase):
    @patch("render.mesh.gl.glDeleteBuffers")
    @patch("render.mesh.gl.glDeleteVertexArrays")
    def test_dispose_releases_gpu_objects_only_once(
        self,
        delete_vertex_arrays,
        delete_buffers,
    ):
        mesh = Mesh.__new__(Mesh)
        mesh._vao = 1
        mesh._vbo = 2
        mesh._ebo = 3

        mesh.dispose()
        mesh.dispose()

        delete_vertex_arrays.assert_called_once_with(1, [1])
        self.assertEqual(delete_buffers.call_count, 2)
        delete_buffers.assert_any_call(1, [2])
        delete_buffers.assert_any_call(1, [3])
        self.assertIsNone(mesh._vao)
        self.assertIsNone(mesh._vbo)
        self.assertIsNone(mesh._ebo)


if __name__ == "__main__":
    unittest.main()
