__all__ = ["Coordinate"]
import math
from abc import ABC

class Coordinate(ABC):
    def __init__(self, x, y, z):
        self.x: int = x
        self.y: int = y
        self.z: int = z

    def __eq__(self, other):
        if not isinstance(other, Coordinate):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def get_world_coordinate(self) -> "Coordinate":
        return Coordinate(math.floor(self.x / 16), self.y, math.floor(self.z / 16))

    def get_chunk_coordinate(self) -> "Coordinate":
        return Coordinate(math.floor(self.x / 16), self.y, math.floor(self.z / 16))

    def get_region_coordinate(self) -> "Coordinate":
        return Coordinate(math.floor(self.x / 512), self.y, math.floor(self.z / 512))


