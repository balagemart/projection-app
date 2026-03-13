from PyQt6.QtWidgets import QDoubleSpinBox, QSpinBox
from PyQt6.QtCore import Qt, QEvent


class DragDoubleSpinBox(QDoubleSpinBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dragging = False
        self._start_y = 0
        self._start_value = 0.0
        self.lineEdit().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.lineEdit():
            if event.type() == QEvent.Type.MouseButtonPress:    # QtEnum
                if event.button() == Qt.MouseButton.LeftButton:
                    self._dragging = True
                    self._start_y = event.globalPosition().y()
                    self._start_value = self.value()
                    return True
            elif event.type() == QEvent.Type.MouseMove and self._dragging:
                current_y = event.globalPosition().y()
                dy = (self._start_y - current_y) / 10

                mod = event.modifiers()
                if mod & Qt.KeyboardModifier.ShiftModifier:
                    factor = 0.1
                elif mod & Qt.KeyboardModifier.ControlModifier:
                    factor = 10.0
                else:
                    factor = 1.0

                new_value = self._start_value + dy * self.singleStep() * factor

                self.setValue(new_value)

                self._start_value = self.value()
                self._start_y = current_y
            elif event.type() == QEvent.Type.MouseButtonRelease:
                self._dragging = False
                return True
        return super().eventFilter(obj, event)


class DragIntSpinBox(QSpinBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._dragging = False
        self._start_y = 0
        self._start_value = 0
        self.lineEdit().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self.lineEdit():
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    self._dragging = True
                    self._start_y = event.globalPosition().y()
                    self._start_value = self.value()
                    return True
            elif event.type() == QEvent.Type.MouseMove and self._dragging:
                current_y = event.globalPosition().y()
                dy = (self._start_y - current_y) / 10

                mod = event.modifiers()
                if mod & Qt.KeyboardModifier.ShiftModifier:
                    factor = 0.1
                elif mod & Qt.KeyboardModifier.ControlModifier:
                    factor = 10.0
                else:
                    factor = 1.0

                new_value = int(self._start_value + dy * self.singleStep() * factor)

                self.setValue(new_value)

                self._start_value = self.value()
                self._start_y = current_y
            elif event.type() == QEvent.Type.MouseButtonRelease:
                self._dragging = False
                return True
        return super().eventFilter(obj, event)
