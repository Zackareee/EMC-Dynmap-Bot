__all__ = ["Coordinate"]

from dataclasses import dataclass


@dataclass
class Coordinate:
    x: int
    z: int
