import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QWidget

from core.camera import OrbitCamera
from editor.viewport_state import ViewportState
from render.gl_viewport import GLViewport
from scene.scene import Scene


class ViewportStateTests(unittest.TestCase):
    def test_defaults_show_grid_and_axes(self):
        state = ViewportState(camera=OrbitCamera())

        self.assertTrue(state.show_grid)
        self.assertTrue(state.show_axes)

    def test_viewport_creates_default_state_from_scene_editor_camera(self):
        scene = Scene()
        viewport = GLViewport()

        viewport.set_scene(scene)

        self.assertIsNotNone(viewport.state)
        self.assertIs(viewport.state.camera, scene.editor_camera)

    def test_viewport_uses_provided_state_and_updates_camera(self):
        first_camera = OrbitCamera()
        second_camera = OrbitCamera()
        state = ViewportState(camera=first_camera, show_grid=False)
        viewport = GLViewport(viewport_state=state)

        viewport.set_current_camera(second_camera)

        self.assertIs(viewport.state, state)
        self.assertIs(viewport.state.camera, second_camera)
        self.assertFalse(viewport.state.show_grid)

    def test_positional_parent_is_not_treated_as_state(self):
        parent = QWidget()
        scene = Scene()
        viewport = GLViewport(parent)

        viewport.set_scene(scene)

        self.assertIs(viewport.parent(), parent)
        self.assertIsNot(viewport.state, parent)
        self.assertIs(viewport.state.camera, scene.editor_camera)

    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])


if __name__ == "__main__":
    unittest.main()
