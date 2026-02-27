from __future__ import annotations

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction


def build_menus(window: QMainWindow, *, on_import_obj) -> None:
    menubar = window.menuBar()
    file_menu = menubar.addMenu("File")

    import_action = QAction("Import OBJ", window)
    import_action.triggered.connect(on_import_obj)

    file_menu.addAction(import_action)
