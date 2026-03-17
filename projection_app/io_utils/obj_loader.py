import numpy as np


def load_obj(path: str) -> tuple[np.ndarray, np.ndarray]:
    vertices: list[list[float]] = []
    faces: list[list[float]] = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("v "):
                parts = line.strip().split()
                vertices.append([
                    float(parts[1]),
                    float(parts[2]),
                    float(parts[3])
                ])
            elif line.startswith("f "):
                parts = line.strip().split()

                face = [int(e.split("/")[0]) - 1
                        for e in parts[1:]]
                faces.append(face)

    vertices = np.array(vertices, dtype=np.float32)
    indices = []
    for face in faces:
        if len(face) == 3:
            indices.extend(face)
        elif len(face) == 4:
            # triangulation
            a, b, c, d = face
            indices.extend([a, b, c,
                            a, c, d])
    indices = np.array(indices, dtype=np.uint32)

    return vertices, indices
