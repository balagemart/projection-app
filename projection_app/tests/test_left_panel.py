import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt6.QtWidgets import QApplication

from scene.scene import Scene
from ui.left_panel import LeftPanel


class LeftPanelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.scene = Scene()
        self.panel = LeftPanel()
        self.panel.set_scene(self.scene)

    def test_cube_properties_include_size_and_transform_rows(self):
        obj_id = self.scene.add_cube()

        self.panel.build_properties(self.scene.get_object(obj_id))

        self.assertEqual(self.panel.properties_layout.rowCount(), 4)

    def test_sphere_properties_include_geometry_and_transform_rows(self):
        obj_id = self.scene.add_sphere()

        self.panel.build_properties(self.scene.get_object(obj_id))

        self.assertEqual(self.panel.properties_layout.rowCount(), 6)


if __name__ == "__main__":
    unittest.main()
