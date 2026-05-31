import tempfile
import unittest
from pathlib import Path

import numpy as np

from io_utils.obj_loader import load_obj


class ObjLoaderTests(unittest.TestCase):
    def test_loads_vertices_and_triangulates_quad_faces(self):
        obj = """\
v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 1.0 1.0 0.0
v 0.0 1.0 0.0
f 1 2 3 4
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "quad.obj"
            path.write_text(obj, encoding="utf-8")

            vertices, indices = load_obj(str(path))

        np.testing.assert_array_equal(
            vertices,
            np.array(
                [
                    [0.0, 0.0, 0.0],
                    [1.0, 0.0, 0.0],
                    [1.0, 1.0, 0.0],
                    [0.0, 1.0, 0.0],
                ],
                dtype=np.float32,
            ),
        )
        np.testing.assert_array_equal(
            indices,
            np.array([0, 1, 2, 0, 2, 3], dtype=np.uint32),
        )

    def test_loads_faces_with_obj_slash_syntax(self):
        obj = """\
v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 0.0 1.0 0.0
f 1/1/1 2/2/1 3/3/1
"""
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "triangle.obj"
            path.write_text(obj, encoding="utf-8")

            _, indices = load_obj(str(path))

        np.testing.assert_array_equal(indices, np.array([0, 1, 2], dtype=np.uint32))


if __name__ == "__main__":
    unittest.main()
