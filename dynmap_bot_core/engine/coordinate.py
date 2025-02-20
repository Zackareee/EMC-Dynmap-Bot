__all__ = ["Coordinate", "Chunk", "Town", "Map", "build_map", "build_town", "build_image_with_map"]
import math
from abc import ABC
from PIL import Image
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

from dynmap_bot_core.download import common
from dynmap_bot_core import download as dl
from dynmap_bot_core.images import image as img


def unpack_town_coordinates(town_json: dict) -> list[list[int,int]]:
    """
    Given a dictionary of a town object, return all coordinates
    :param town_json: Town object as a dictionary.
    :return: list of ints for all coordinates.
    """
    coordinates: list[list[int,int]] = [town_json["coordinates"]["townBlocks"]]
    return coordinates

def ensure_multipolygon(geometry: Polygon | MultiPolygon) -> MultiPolygon:
    """
     Convert a Polygon to a MultiPolygon if it isn't one already.
    :param geometry: A possible Polygon or Multipolygon.
    :return:
    """
    if isinstance(geometry, Polygon):
        return MultiPolygon([geometry])
    elif isinstance(geometry, MultiPolygon):
        return geometry
    else:
        raise TypeError("Input geometry must be a Polygon or MultiPolygon.")


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


class Chunk(Coordinate):
    SIZE = 16

    def __init__(self, x, y, z):
        # The bottom right of a chunk
        # IE its max coordinate
        super().__init__(x * 16, y, z * 16)


class Town:
    def __init__(self, chunks):
        self.chunks: [Chunk] = chunks

    def offset_chunks(self, x, y, z) -> "Town":
        """
        Offsets all chunks within a town by given x, y, z factors.
        :return: Returns a new Town object.
        """
        _chunks = []
        for chunk in self.chunks:
            _chunks.append(Coordinate(x=chunk.x + x, y=chunk.y + y, z=chunk.z + z))
        return Town(chunks=_chunks)

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

    def as_polygon(self) -> MultiPolygon:
        """
        Returns the town as a MultiPolygon object where the bounds of the polygon(s) are the border(s) of the town.
        :return:
        """
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

    def get_regions(self) -> set[Coordinate]:
        """
        Gets all unique regions the Town is within as Coordinates.
        """
        # To account for regions that are non-rectangular shaped,
        # dedupe all the regions for all included chunks.
        return set(chunk.get_region_coordinate() for chunk in self.chunks)

class Nation(Town):
    pass

class Map:
    """
    A map is a collection of Towns.
    """

    def __init__(self, towns):
        self.towns: [Town] = towns

    def get_polygon_top_left_corner(self) -> Coordinate:
        """
        Gets the upper left most coordinate of the map.
        :return:
        """
        return Coordinate(
            x=min(t.get_polygon_top_left_corner().x for t in self.towns),
            y=0,
            z=min(t.get_polygon_top_left_corner().z for t in self.towns),
        )

    def get_polygon_bottom_right_corner(self) -> Coordinate:
        """
        Gets the bottom right most coordinate of the map.
        :return:
        """
        return Coordinate(
            x=max(t.get_polygon_bottom_right_corner().x for t in self.towns),
            y=0,
            z=max(t.get_polygon_bottom_right_corner().z for t in self.towns),
        )

    def offset_towns(self, x, y, z) -> "Map":
        """
        Offsets all towns within the map by given x, y, z factors.
        :return: Returns a new Map object.
        """
        _towns = []
        for town in self.towns:
            _towns.append(town.offset_chunks(x, y, z))
        return Map(_towns)

    def get_normalised_map(self) -> "Map":
        """
        Shifts all towns on the map, such that the top left most coordinate of the Towns are now (0, 0)
        This is necessary for PIL to paste the polygons in the bounds of an image.
        :return:
        """
        offset_x = self.get_polygon_top_left_corner().x
        offset_z = self.get_polygon_top_left_corner().z
        return self.offset_towns(-offset_x, 0, -offset_z)

    def get_town_polygons(self) -> list[Polygon]:
        """
        Returns the polygons for each town.
        :return:
        """
        return [
            polygon
            for multi_polygon in self.towns
            for polygon in multi_polygon.as_polygon().geoms
        ]

    def get_region_offset(self) -> list[int]:
        """
        Gets the maps offset from the nearest region border
        """
        minimum_coordinate: Coordinate = self.get_polygon_top_left_corner()
        x_offset: int = minimum_coordinate.x % 512
        z_offset: int = minimum_coordinate.z % 512
        offset: list[int] = [x_offset, z_offset]
        return offset

    def get_regions(self) -> list[Coordinate]:
        """
        Gets all unique regions the Map is within as Coordinates.
        :return:
        """
        regions = set()
        for town in self.towns:
            towns_regions: set[Coordinate] = town.get_regions()
            [regions.add(coord) for coord in towns_regions]
        return list(regions)

# TODO build an abstraction on town so nations and towns can be mixed - Maybe a bad idea since a town and nation can
#  have the same name
def build_town(town_name: str) -> Town:
    """
    Returns a town object given the town name.
    :param town_name:
    :return:
    """
    town: list[list[int,int]] = unpack_town_coordinates(common.download_town(town_name))
    return Town([Chunk(x, 0, z) for x, z in town[0]])


def build_map(town_names: list[str]) -> Map:
    """
    Returns a Map object given the town names.
    :param town_names:
    :return:
    """
    return Map([build_town(town) for town in town_names])


def build_image_with_map(map_obj: Map) -> Image:
    """
    Prepares the map object, aligns polygons as needed, downloads images, and overlays polygons ontop. Lots going on.
    TODO refactor this - the current setup will not work with nations
    :param map_obj: a map object
    :return: an Image object with the polygon overlayed ontop of the background
    """
    map_regions: list[Coordinate] = list(map_obj.get_regions())

    normalised_map = map_obj.get_normalised_map()
    offset = map_obj.get_region_offset()
    map_multipolygon: Map = normalised_map.offset_towns(offset[0], 0, offset[1])

    image_data = dl.map_images_as_dict(map_regions)

    image: Image = img.make_image_collage(image_data)

    for map_polygon in map_multipolygon.get_town_polygons():
        image = img.make_grids_on_collage(map_polygon, image)

    return image


