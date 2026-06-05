from dataclasses import dataclass

from core.camera import Camera


@dataclass
class ViewportState:
    camera: Camera
    show_grid: bool = True
    show_axes: bool = True
