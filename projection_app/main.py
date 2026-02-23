import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

from PyQt6.QtGui import QSurfaceFormat
# from PyQt6.QtOpenGLWidgets import QOpenGLWidget


def main():
    # MSAA
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
    fmt.setSamples(8)   # 8x MSAA
    QSurfaceFormat.setDefaultFormat(fmt)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # start of the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
