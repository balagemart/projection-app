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

# general
DEFAULT_NAME: str = ""

# cube
DEFAULT_CUBE_SIZE: float = 3.0

# sphere
DEFAULT_SPHERE_RADIUS: float = 2.0
DEFAULT_STACKS: int = 100
DEFAULT_SLICES: int = 100


def create_cube(
    size: float = DEFAULT_CUBE_SIZE,
    name: str = DEFAULT_NAME
) -> SceneObject:
    return SceneObject(
        id=0,
        name=name,
        obj_type=ObjectType.CUBE,
        geometry=CubeGeometry(size=float(size)),
    )


def create_sphere(
    radius: float = DEFAULT_SPHERE_RADIUS,
    *,
    stacks: int = DEFAULT_STACKS,
    slices: int = DEFAULT_SLICES,
    name: str = DEFAULT_NAME,
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
