import numpy as np


def load_obj(path: str):
    vertices = []
    faces = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("v "):
                line_elements = line.strip().split()
                vertices.append([
                                float(line_elements[1]),
                                float(line_elements[2]),
                                float(line_elements[3])
                                ])
            elif line.startswith("f "):
                line_elements = line.strip().split()
                face = [int(e.split("/")[0]) - 1 for e in line_elements[1:]]
                faces.append(face)
    vertices = np.array(vertices, dtype=np.float32)

    indices = []
    for face in faces:
        if len(face) == 3:
            indices.extend(face)
        elif len(face) == 4:
            # triangulation
            indices.extend([face[0], face[1], face[2],
                            face[0], face[2], face[3]])
    indices = np.array(indices, dtype=np.uint32)
    return vertices, indices
