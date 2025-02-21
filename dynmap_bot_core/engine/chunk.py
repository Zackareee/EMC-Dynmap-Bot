__all__ = ["Chunk"]
from dynmap_bot_core.engine import coordinate

class Chunk(coordinate.Coordinate):
    SIZE = 16

    def __init__(self, x, y, z):
        # The bottom right of a chunk
        # IE its max coordinate
        super().__init__(x * self.SIZE, y, z * self.SIZE)
