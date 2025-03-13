__all__ = ["Town"]
from dynmap_bot_core.models.spatial.chunk import Chunk
from dynmap_bot_core.models.spatial.coordinate import Coordinate
from dynmap_bot_core.models.color_polygon import (
    ColorPolygon,
    ColorMultiPolygon,
    colored_unary_union,
)


class Town:
    def __init__(self, chunks):
        self.chunks: [Chunk] = chunks
        self.color: str = "03D7FC"
        self.nation_name: str | None = None

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
            x=min(chunk.x for chunk in self.chunks) - padding,
            y=0,
            z=min(chunk.z for chunk in self.chunks) - padding,
        )

    def get_polygon_bottom_right_corner(self) -> Coordinate:
        """
        Helper function to get the bottom right most corner, useful for maximum coordinates of a town.
        Coordinate location may not necessarily within the bounds of the town, but instead representative of its bottom
        right most corner.
        :return:
        """
        return Coordinate(
            x=max(chunk.x for chunk in self.chunks),
            y=0,
            z=max(chunk.z for chunk in self.chunks),
        )

    def as_polygon(self, color: str) -> ColorMultiPolygon:
        """
        Returns the town as a MultiPolygon object where the bounds of the polygon(s) are the border(s) of the town.
        :return:
        """
        polygons: [ColorPolygon] = [chunk.as_polygon(color) for chunk in self.chunks]
        unary_polygon: ColorMultiPolygon = colored_unary_union(polygons)
        return unary_polygon

    def get_regions(self) -> set[Coordinate]:
        """
        Gets all unique regions the Town is within as Coordinates.
        """
        # To account for regions that are non-rectangular shaped,
        # dedupe all the regions for all included chunks.
        return set(chunk.get_region_coordinate() for chunk in self.chunks)
