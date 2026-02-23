from __future__ import annotations
from dataclasses import dataclass, field

from core.camera import OrbitCamera


@dataclass
class Scene:
    """
    Minimál jelenet (Scene) – csak az app "világállapota".
    Most: 1 db kamera.
    Később: pontok, objektumok, kijelölés, stb.
    """
    camera: OrbitCamera = field(default_factory=OrbitCamera)
