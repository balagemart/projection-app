from dataclasses import dataclass


@dataclass(frozen=True)
class ObjectLink:
    start_id: int
    end_id: int
