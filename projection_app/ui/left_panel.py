import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QFormLayout,
    QDoubleSpinBox, QSpinBox, QListWidgetItem, QHBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from scene.scene import Scene, SceneObject


class LeftPanel(QWidget):

    scene_changed = pyqtSignal()         # event with int value

    def __init__(self):
        super().__init__()
        self.setObjectName("LeftPanel")
        self.setAutoFillBackground(True)

        self.scene: Scene | None = None
        self.current_object: SceneObject | None = None

        layout = QVBoxLayout(self)

        # object list
        layout.addWidget(QLabel("Objects"))

        self.list_widget = QListWidget(self)
        layout.addWidget(self.list_widget)

        # properties area
        layout.addWidget(QLabel("Properties"))

        self.properties_widget = QWidget(self)
        layout.addWidget(self.properties_widget)

        self.properties_layout = QFormLayout(self.properties_widget)

        # signals
        self.list_widget.currentItemChanged.connect(self.on_selection_changed)

    def set_scene(self, scene: Scene):
        self.scene = scene

    def refresh_objects(self):
        if self.scene is None:
            return

        self.list_widget.clear()

        for obj in self.scene.objects:
            item = QListWidgetItem(obj.name)
            item.setData(Qt.ItemDataRole.UserRole, obj.id)
            self.list_widget.addItem(item)

        if self.scene.selected_id is not None:
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                if item.data(Qt.ItemDataRole.UserRole) == self.scene.selected_id:
                    self.list_widget.setCurrentItem(item)
                    break   # TODO BREAK NELKUL MAJD

    def clear_properties(self):
        while self.properties_layout.rowCount():
            self.properties_layout.removeRow(0)

    def _generate_xyz_spinboxes(
            self,
            values,
            *,
            min_value: float,
            max_value: float,
            step: float,
            decimals: int = 3
    ):
        row_widget = QWidget(self)
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(6)

        spins = []
        prefixes = ["X ", "Y ", "Z "]
        for prefix, value in zip(prefixes, values):
            spin = QDoubleSpinBox(self)
            spin.setRange(min_value, max_value)
            spin.setDecimals(decimals)
            spin.setSingleStep(step)
            spin.setValue(float(value))
            spin.setPrefix(prefix)
            row_layout.addWidget(spin)
            spins.append(spin)

        return row_widget, spins

    def build_properties(self, obj: SceneObject):
        self.clear_properties()
        self.current_object = obj
        if obj.type == "cube":
            self._build_cube_properties(obj)
        elif obj.type == "sphere":
            self._build_sphere_properties(obj)
        elif obj.type == "imported":
            self._build_imported_properties(obj)

        self._build_transform_properties(obj)

    def on_position_changed(self, axis: int, value: float) -> None:
        if self.current_object is None:
            return

        self.current_object.position[axis] = float(value)
        self.current_object.transform_dirty = True
        self.scene_changed.emit()

    def on_rotation_changed(self, axis: int, value: float) -> None:
        if self.current_object is None:
            return None

        self.current_object.rotation[axis] = float(np.deg2rad(value))
        self.current_object.transform_dirty = True
        self.scene_changed.emit()

    def on_scale_changed(self, axis: int, value: float) -> None:
        if self.current_object is None:
            return

        self.current_object.scale[axis] = float(value)
        self.current_object.transform_dirty = True
        self.scene_changed.emit()

    def _build_transform_properties(self, obj: SceneObject):
        pos_row, pos_spins = self._generate_xyz_spinboxes(
                    obj.position,
                    min_value=-1000.0,
                    max_value=1000.0,
                    step=0.1,
                )
        rot_deg = [np.rad2deg(v) for v in obj.rotation]
        rot_row, rot_spins = self._generate_xyz_spinboxes(
                    rot_deg,
                    min_value=-360.0,
                    max_value=360.0,
                    step=0.1,
                )
        scale_row, scale_spins = self._generate_xyz_spinboxes(
                    obj.scale,
                    min_value=0.01,
                    max_value=1000.0,
                    step=0.1
                )

        pos_spins[0].valueChanged.connect(lambda v: self.on_position_changed(0, v))
        pos_spins[1].valueChanged.connect(lambda v: self.on_position_changed(1, v))
        pos_spins[2].valueChanged.connect(lambda v: self.on_position_changed(2, v))

        rot_spins[0].valueChanged.connect(lambda v: self.on_rotation_changed(0, v))
        rot_spins[1].valueChanged.connect(lambda v: self.on_rotation_changed(1, v))
        rot_spins[2].valueChanged.connect(lambda v: self.on_rotation_changed(2, v))

        scale_spins[0].valueChanged.connect(lambda v: self.on_scale_changed(0, v))
        scale_spins[1].valueChanged.connect(lambda v: self.on_scale_changed(1, v))
        scale_spins[2].valueChanged.connect(lambda v: self.on_scale_changed(2, v))

        self.properties_layout.addRow("Position", pos_row)
        self.properties_layout.addRow("Rotation", rot_row)
        self.properties_layout.addRow("Scale", scale_row)

    def on_selection_changed(
            self,
            current: QListWidgetItem | None,
            previous: QListWidgetItem | None
            ) -> None:
        if self.scene is None:
            return

        if current is None:
            self.current_object = None
            self.scene.select(None)
            self.clear_properties()
            return

        obj_id = current.data(Qt.ItemDataRole.UserRole)
        obj = self.scene.get_object(obj_id)

        if obj is None:
            self.current_object = None
            self.scene.select(None)
            self.clear_properties()
            return

        self.scene.select(obj.id)
        self.build_properties(obj)

    def _build_cube_properties(self, obj: SceneObject):
        size_spin = QDoubleSpinBox()
        size_spin.setRange(0.1, 1000.0)
        size_spin.setDecimals(3)
        size_spin.setSingleStep(0.1)
        size_spin.setValue(float(obj.params["size"]))

        size_spin.valueChanged.connect(self.on_cube_size_changed)

        self.properties_layout.addRow("Size", size_spin)

    def _build_sphere_properties(self, obj: SceneObject):
        radius_spin = QDoubleSpinBox(self)
        radius_spin.setRange(0.1, 1000.0)
        radius_spin.setDecimals(3)
        radius_spin.setSingleStep(0.1)
        radius_spin.setValue(float(obj.params["radius"]))

        slices_spin = QSpinBox(self)
        slices_spin.setRange(3, 500)
        slices_spin.setValue(int(obj.params["slices"]))

        stacks_spin = QSpinBox(self)
        stacks_spin.setRange(3, 500)
        stacks_spin.setValue(int(obj.params["stacks"]))

        radius_spin.valueChanged.connect(self.on_sphere_radius_changed)
        slices_spin.valueChanged.connect(self.on_sphere_slices_changed)
        stacks_spin.valueChanged.connect(self.on_sphere_stacks_changed)

        self.properties_layout.addRow("Radius", radius_spin)
        self.properties_layout.addRow("Slices", slices_spin)
        self.properties_layout.addRow("Stacks", stacks_spin)

    def _build_imported_properties(self, obj: SceneObject):
        size = QDoubleSpinBox()
        # TODO matrix szorzassal size noveles

    # property change handlers
    def on_cube_size_changed(self, value: float) -> None:
        if self.current_object is None:
            return

        self.current_object.params["size"] = float(value)
        self.current_object.geometry_dirty = True
        self.scene_changed.emit()

    def on_sphere_radius_changed(self, value: float) -> None:
        if self.current_object is None:
            return

        self.current_object.params["radius"] = float(value)
        self.current_object.geometry_dirty = True
        self.scene_changed.emit()

    def on_sphere_stacks_changed(self, value: float) -> None:
        if self.current_object is None:
            return

        self.current_object.params["stacks"] = int(value)
        self.current_object.geometry_dirty = True
        self.scene_changed.emit()

    def on_sphere_slices_changed(self, value: int) -> None:
        if self.current_object is None:
            return

        self.current_object.params["slices"] = int(value)
        self.current_object.geometry_dirty = True
        self.scene_changed.emit()
