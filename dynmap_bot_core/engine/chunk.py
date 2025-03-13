__all__ = ["Chunk"]
from dynmap_bot_core.engine import coordinate
from dynmap_bot_core.engine.colorpolygon import ColorPolygon


class Chunk(coordinate.Coordinate):
    SIZE = 16

    def as_polygon(self, color: str) -> ColorPolygon:
        """
        Returns a polygon in the shape of a square, with a length and width of self.SIZE where self.x and self.z are the
        center point of the square.
        Sets the color to 50% opacity. ie. (#??????7F)
        :param color: a hexadecimal string representing a color
        :return: a ColorPolygon representation of the square
        """
        padding = self.SIZE / 2
        polygon = ColorPolygon(
            color=f"{color}7F",
            shell=[
                (self.x - padding, self.z - padding),
                (self.x - padding, self.z + padding),
                (self.x + padding, self.z + padding),
                (self.x + padding, self.z - padding),
            ],
        )
        return polygon

    def __init__(self, x, y, z):
        # The bottom right of a chunk
        # IE its max coordinate
        super().__init__(x * self.SIZE, y, z * self.SIZE)
