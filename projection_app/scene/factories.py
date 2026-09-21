import numpy as np

from core.camera import SceneCamera
from geometry.sources import (
    PointGeometry,
    LineGeometry,
    CameraGeometry,
    CubeGeometry,
    ImportedGeometry,
    SphereGeometry,
    FrustumGeometry,
    PointCloudGeometry
)
from scene.entity import ObjectType, SceneObject
from scene.transform import Transform
from scene.links import ObjectLink
from core.camera import ProjectionMode

# general
DEFAULT_NAME: str = ""

# point
DEFAULT_POINT_SIZE: float = 0.05

# cube
DEFAULT_CUBE_SIZE: float = 3.0

# sphere
DEFAULT_SPHERE_RADIUS: float = 2.0
DEFAULT_STACKS: int = 100
DEFAULT_SLICES: int = 100


def create_point(
    size: float = DEFAULT_POINT_SIZE,
    name: str = DEFAULT_NAME
) -> SceneObject:
    return SceneObject(
        id=0,
        name=name,
        obj_type=ObjectType.POINT,
        geometry=PointGeometry(size=float(size)),
        made_of_triangles=False
    )


def create_pointcloud(
    points: np.ndarray,
    name: str = DEFAULT_NAME
) -> SceneObject:
    return SceneObject(
        id=0,
        name=name,
        obj_type=ObjectType.POINTCLOUD,
        geometry=PointCloudGeometry(points),
        made_of_triangles=False
    )


def create_line_between(
        start_id: int,
        end_id: int,
        name: str = DEFAULT_NAME
) -> SceneObject:
    return SceneObject(
        id=0,
        name=name,
        obj_type=ObjectType.LINE,
        link=ObjectLink(start_id=start_id, end_id=end_id),
        made_of_triangles=False
    )


def create_cube(
    size: float = DEFAULT_CUBE_SIZE,
    name: str = DEFAULT_NAME
) -> SceneObject:
    return SceneObject(
        id=0,
        name=name,
        obj_type=ObjectType.CUBE,
        geometry=CubeGeometry(size=float(size)),
        made_of_triangles=True
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
        made_of_triangles=True
    )


def create_persp_camera(name: str = "") -> SceneObject:
    transform = Transform()

    return SceneObject(
        id=0,
        name=name,
        obj_type=ObjectType.PERSP_CAMERA,
        geometry=CameraGeometry(),
        camera=SceneCamera(transform=transform, projection_mode=ProjectionMode.PERSPECTIVE),
        transform=transform,
        made_of_triangles=False
    )


def create_ortho_camera(name: str = "") -> SceneObject:
    transform = Transform()

    return SceneObject(
        id=0,
        name=name,
        obj_type=ObjectType.ORTHO_CAMERA,
        geometry=CameraGeometry(),
        camera=SceneCamera(transform=transform, projection_mode=ProjectionMode.ORTHOGRAPHIC),
        transform=transform,
        made_of_triangles=False
    )


def create_frustum(
    cam_id: float,
    cam: SceneCamera,
    aspect: float,
    name: str = ""
) -> SceneObject:

    forward, right, up = cam.basis_vectors()
    right = np.cross(forward, up)
    right = right / np.linalg.norm(right)
    ortho_scale = cam.ortho_scale

    return SceneObject(
        id=0,
        name=name,
        obj_type=ObjectType.FRUSTUM,
        link=ObjectLink(start_id=cam_id, end_id=-1),
        geometry=FrustumGeometry(
            cam.transform.position,
            forward,
            right,
            up,
            cam.projection_mode,
            np.deg2rad(cam.fov_y_deg),
            ortho_scale,
            aspect,
            cam.near,
            cam.far
        ),
        made_of_triangles=False
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
        made_of_triangles=True
    )
