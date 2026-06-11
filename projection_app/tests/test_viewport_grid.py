import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication

from core.camera import OrbitCamera, ProjectionMode, ViewMode
from scene.scene import Scene
from ui.right_panel import RightPanel
from ui.viewport_grid import ViewportGrid, ViewportGridMode, ViewportId


class ViewportGridTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def test_creates_four_viewports_with_perspective_active_by_default(self):
        scene = Scene()
        grid = ViewportGrid(scene)

        self.assertEqual(len(grid.viewports), 4)
        self.assertEqual(grid.current_viewport_mode, ViewportGridMode.SINGLE)
        self.assertIsNotNone(grid.active_viewport)
        self.assertIsNot(grid.active_viewport.state.camera, scene.editor_camera)
        self.assertEqual(
            grid.active_viewport.state.camera.projection_mode,
            ProjectionMode.PERSPECTIVE,
        )

    def test_fixed_viewports_use_expected_editor_views(self):
        scene = Scene()
        grid = ViewportGrid(scene)

        self.assertEqual(
            grid._viewports[ViewportId.FRONT].state.camera.view_mode,
            ViewMode.FRONT,
        )
        self.assertEqual(
            grid._viewports[ViewportId.TOP].state.camera.view_mode,
            ViewMode.TOP,
        )
        self.assertEqual(
            grid._viewports[ViewportId.RIGHT].state.camera.view_mode,
            ViewMode.RIGHT,
        )

    def test_forwards_camera_to_active_viewport(self):
        scene = Scene()
        grid = ViewportGrid(scene)
        camera = OrbitCamera()

        grid.set_current_camera(camera)

        self.assertIs(grid.active_viewport.state.camera, camera)

    def test_right_panel_keeps_viewport_compatibility_property(self):
        scene = Scene()
        panel = RightPanel(scene)

        self.assertIs(panel.viewport, panel.viewport_grid.active_viewport)

    def test_toggle_mode_switches_between_single_and_quad(self):
        scene = Scene()
        grid = ViewportGrid(scene)

        grid.toggle_mode()
        self.assertEqual(grid.current_viewport_mode, ViewportGridMode.QUAD)

        grid.toggle_mode()
        self.assertEqual(grid.current_viewport_mode, ViewportGridMode.SINGLE)


if __name__ == "__main__":
    unittest.main()
