import numpy as np

from core.camera import SceneCamera
from geometry.sources import (
    CameraGeometry,
    CubeGeometry,
    ImportedGeometry,
    SphereGeometry,
)
from scene.entity import ObjectType, SceneObject
from scene.transform import Transform


def create_cube(size: float = 3.0, name: str = "") -> SceneObject:
    return SceneObject(
        id=0,
        name=name,
        obj_type=ObjectType.CUBE,
        geometry=CubeGeometry(size=float(size)),
    )


def create_sphere(
    radius: float = 2.0,
    *,
    stacks: int = 100,
    slices: int = 100,
    name: str = "",
) -> SceneObject:
    return SceneObject(
        id=0,
        name=name,
        obj_type=ObjectType.SPHERE,
        geometry=SphereGeometry(
            radius=float(radius),
            stacks=int(stacks),
            slices=int(slices),
        ),
    )


def create_camera(name: str = "") -> SceneObject:
    transform = Transform()

    return SceneObject(
        id=0,
        name=name,
        obj_type=ObjectType.CAMERA,
        geometry=CameraGeometry(),
        camera=SceneCamera(transform=transform),
        transform=transform,
    )


def create_imported_mesh(
    vertices: np.ndarray,
    indices: np.ndarray | None,
    *,
    components_per_vertex: int = 3,
    name: str = "",
) -> SceneObject:
    return SceneObject(
        id=0,
        name=name,
        obj_type=ObjectType.IMPORTED,
        geometry=ImportedGeometry(
            vertices=vertices,
            indices=indices,
            components_per_vertex=int(components_per_vertex),
        ),
    )
