import math
from collections import namedtuple
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from abc import ABC


def ensure_multipolygon(geometry):
    """
    Convert a Polygon to a MultiPolygon if it isn't one already.
    """
    if isinstance(geometry, Polygon):
        return MultiPolygon([geometry])
    elif isinstance(geometry, MultiPolygon):
        return geometry
    else:
        raise TypeError("Input geometry must be a Polygon or MultiPolygon.")


class Location(ABC):
    def __init__(self, x, y, z):
        self.x: float = x
        self.y: float = y
        self.z: float = z

    def __eq__(self, other):
        if not isinstance(other, Location):
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


class Coordinate(Location):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)


class Chunk(Location):
    SIZE = 16

    def __init__(self, x, y, z):
        # The bottom right of a chunk
        # IE its max coordinate
        super().__init__(x * 16, y, z * 16)


class Town:
    def __init__(self, chunks):
        self.chunks: [Chunk] = chunks

    def get_polygon_top_left_corner(self):
        padding = Chunk.SIZE
        return Coordinate(
            x=min(c.x for c in self.chunks) - padding,
            y=0,
            z=min(c.z for c in self.chunks) - padding,
        )

    def get_polygon_bottom_right_corner(self):
        return Coordinate(
            x=max(c.x for c in self.chunks), y=0, z=max(c.z for c in self.chunks)
        )

    def as_polygon(self):
        padding = Chunk.SIZE / 2
        unary_polygon = unary_union(
            [
                Polygon(
                    [
                        (c.x - padding, c.z - padding),
                        (c.x - padding, c.z + padding),
                        (c.x + padding, c.z + padding),
                        (c.x + padding, c.z - padding),
                    ]
                )
                for c in self.chunks
            ]
        )
        return ensure_multipolygon(unary_polygon)

    def get_regions(self):
        # To account for regions that are non-rectangular shaped,
        # dedupe all the regions for all included chunks.
        return set(chunk.get_region_coordinate() for chunk in self.chunks)


class Map:
    """
    A map is a collection of Towns.
    """

    def __init__(self, towns):
        self.towns: [Town] = towns

    def get_polygon_top_left_corner(self):
        return Coordinate(
            x=min(t.get_polygon_top_left_corner().x for t in self.towns),
            y=0,
            z=min(t.get_polygon_top_left_corner().z for t in self.towns),
        )

    def get_polygon_bottom_right_corner(self):
        return Coordinate(
            x=max(t.get_polygon_bottom_right_corner().x for t in self.towns),
            y=0,
            z=max(t.get_polygon_bottom_right_corner().z for t in self.towns),
        )

    def get_town_polygons(self, normalised=False, offset_x=0, offset_y=0) -> [Polygon]:
        """
        Returns the polygons for each town.

        If normalised is set to True, the polygons are coordinates are offset to positive integers only, as
        the polygon drawing library does not support negative coordinates.
        :return:
        """
        polygons = [polygon for multi_polygon in self.towns for polygon in multi_polygon.as_polygon().geoms]

        if not normalised:
            return polygons

        if normalised:
            offset_x -= self.get_polygon_top_left_corner().x
            offset_y -= self.get_polygon_top_left_corner().z

        return [offset_polygon(offset_x, offset_y, p) for p in polygons]

    def get_offset_map(self, offset_x, offset_z):
        return self.get_town_polygons(True, offset_x, offset_z)

    def get_region_offset(self):
        """gets the maps offset from the nearest region border"""
        minimum_coordinate = self.get_polygon_top_left_corner()
        x_offset = minimum_coordinate.x % 512
        z_offset = minimum_coordinate.z % 512
        return [x_offset, z_offset]


    def get_regions(self) -> [[int, int]]:
        regions = set()
        for town in self.towns:
            [regions.add(i) for i in town.get_regions()]
        return list(regions)



# Coordinate = namedtuple('Coordinate', ['x', 'y', 'z'])


def offset_polygon(offset_x, offset_y, polygon):
    return Polygon([(x + offset_x, y + offset_y) for x, y in polygon.exterior.coords])


# class Cell(ABC):
#     """
#     A unit of space in Minecraft of at least one coordinate.
#     Represented using the centre, width and height of the cell, as seen from above.
#     """
#     def __init__(self, centre: Coordinate, width, height):
#         self.centre = centre
#         self.width = width
#         self.height = height
#
# class Region(Cell):
#     def __init__(self, centre):
#         super().__init__(centre, 512, 512)
#
# class Chunk(Cell):
#     def __init__(self, centre):
#         super().__init__(centre, 16, 16)
#
#     def get_region(self) -> Region:
#         """
#         Returns the region this chunk is a part of.
#         """
#         return Region(Coordinate(math.floor(self.centre.x / 32), 0, math.floor(self.centre.z / 32)))

