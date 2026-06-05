import unittest
from unittest.mock import Mock, patch

import numpy as np

from editor.viewport_state import ViewportState
from render.renderer import Renderer
from scene.scene import Scene


class RendererTests(unittest.TestCase):
    @patch("render.renderer.Mesh")
    def test_rebuild_scene_disposes_old_meshes_and_builds_new_ones(self, mesh_class):
        renderer = Renderer()
        old_mesh = Mock()
        renderer._meshes.append(old_mesh)
        scene = Scene()
        scene.add_cube()

        renderer.rebuild_scene(scene)

        old_mesh.dispose.assert_called_once_with()
        mesh_class.assert_called_once()
        self.assertEqual(renderer._meshes, [mesh_class.return_value])

    @patch("render.renderer.Mesh")
    def test_rebuild_scene_does_not_build_normals_for_camera_icon(self, mesh_class):
        renderer = Renderer()
        scene = Scene()
        camera = scene.get_object(scene.add_camera())
        camera.show_normals = True

        renderer.rebuild_scene(scene)

        mesh_class.assert_called_once()

    @patch("render.renderer.gl.glDeleteProgram")
    def test_dispose_releases_meshes_overlays_and_program(self, delete_program):
        renderer = Renderer()
        scene_mesh = Mock()
        grid = Mock()
        axes = Mock()
        renderer._meshes.append(scene_mesh)
        renderer.grid = grid
        renderer.axes = axes
        renderer._program = 17

        renderer.dispose()

        scene_mesh.dispose.assert_called_once_with()
        grid.dispose.assert_called_once_with()
        axes.dispose.assert_called_once_with()
        delete_program.assert_called_once_with(17)
        self.assertEqual(renderer._meshes, [])
        self.assertIsNone(renderer.grid)
        self.assertIsNone(renderer.axes)
        self.assertIsNone(renderer._program)

    @patch("render.renderer.gl.glUseProgram")
    @patch("render.renderer.gl.glUniformMatrix4fv")
    @patch("render.renderer.gl.glClear")
    def test_draw_uses_camera_and_draws_overlays_and_scene_meshes(
        self,
        clear,
        uniform_matrix,
        use_program,
    ):
        renderer = Renderer()
        renderer._program = 23
        renderer._u_mvp_loc = 5
        renderer.grid = Mock()
        renderer.axes = Mock()
        scene_mesh = Mock()
        renderer._meshes.append(scene_mesh)
        camera = Mock()
        camera.projection_matrix.return_value = np.eye(4, dtype=np.float32)
        camera.view_matrix.return_value = np.eye(4, dtype=np.float32)
        state = ViewportState(camera=camera)

        renderer.draw(state, aspect=16 / 9)

        clear.assert_called_once()
        uniform_matrix.assert_called_once()
        use_program.assert_any_call(23)
        use_program.assert_any_call(0)
        renderer.grid.draw.assert_called_once_with()
        renderer.axes.draw.assert_called_once_with()
        scene_mesh.draw.assert_called_once_with()

    @patch("render.renderer.gl.glUseProgram")
    @patch("render.renderer.gl.glUniformMatrix4fv")
    @patch("render.renderer.gl.glClear")
    def test_draw_respects_overlay_visibility(
        self,
        clear,
        uniform_matrix,
        use_program,
    ):
        renderer = Renderer()
        renderer._program = 23
        renderer._u_mvp_loc = 5
        renderer.grid = Mock()
        renderer.axes = Mock()
        camera = Mock()
        camera.projection_matrix.return_value = np.eye(4, dtype=np.float32)
        camera.view_matrix.return_value = np.eye(4, dtype=np.float32)
        state = ViewportState(camera=camera, show_grid=False, show_axes=False)

        renderer.draw(state, aspect=16 / 9)

        renderer.grid.draw.assert_not_called()
        renderer.axes.draw.assert_not_called()


if __name__ == "__main__":
    unittest.main()
