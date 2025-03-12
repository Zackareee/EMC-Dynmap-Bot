__all__ = ["Town"]
from dynmap_bot_core.engine.chunk import Chunk
from dynmap_bot_core.engine.coordinate import Coordinate
from dynmap_bot_core.engine.colorpolygon import (
    ColorPolygon,
    ColorMultiPolygon,
    colored_unary_union,
)


class Town:
    def __init__(self, chunks):
        self.chunks: [Chunk] = chunks
        self.color: str = "03D7FC"
        self.nation_name: str = None

    def offset_chunks(self, x, y, z) -> None:
        """
        Offsets all chunks within a town by given x, y, z factors.
        :return: Returns a new Town object.
        """
        _chunks = []
        for chunk in self.chunks:
            chunk.x = chunk.x + x
            chunk.y = chunk.y + y
            chunk.z = chunk.z + z

    def get_polygon_top_left_corner(self) -> Coordinate:
        """
        Helper function to get the upper left most Coordinate of a town, useful for minimum coordinates of a town.
        Coordinate location may not necessarily within the bounds of the town, but instead representative of its upper
        left most corner.
        :return:
        """
        padding: int = Chunk.SIZE
        return Coordinate(
            x=min(c.x for c in self.chunks) - padding,
            y=0,
            z=min(c.z for c in self.chunks) - padding,
        )

    def get_polygon_bottom_right_corner(self) -> Coordinate:
        """
        Helper function to get the bottom right most corner, useful for maximum coordinates of a town.
        Coordinate location may not necessarily within the bounds of the town, but instead representative of its bottom
        right most corner.
        :return:
        """
        return Coordinate(
            x=max(c.x for c in self.chunks), y=0, z=max(c.z for c in self.chunks)
        )

    def as_polygon(self, color: str) -> ColorMultiPolygon:
        """
        Returns the town as a MultiPolygon object where the bounds of the polygon(s) are the border(s) of the town.
        :return:
        """
        padding = Chunk.SIZE / 2
        unary_polygon = colored_unary_union(
            [
                ColorPolygon(
                    f"{color}7F",
                    [
                        (c.x - padding, c.z - padding),
                        (c.x - padding, c.z + padding),
                        (c.x + padding, c.z + padding),
                        (c.x + padding, c.z - padding),
                    ],
                )
                for c in self.chunks
            ]
        )
        return unary_polygon

    def get_regions(self) -> set[Coordinate]:
        """
        Gets all unique regions the Town is within as Coordinates.
        """
        # To account for regions that are non-rectangular shaped,
        # dedupe all the regions for all included chunks.
        return set(chunk.get_region_coordinate() for chunk in self.chunks)
