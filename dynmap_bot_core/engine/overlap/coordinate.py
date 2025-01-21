import math
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from abc import ABC
from dynmap_bot_core.api_hook import common
from dynmap_bot_core.orm import orm
from dynmap_bot_core import download as dl
from dynmap_bot_core.images import image as img
import PIL


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


class Coordinate(ABC):
    def __init__(self, x, y, z):
        self.x: float = x
        self.y: float = y
        self.z: float = z

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

    def offset_chunks(self, x, y, z):
        _chunks = []
        for chunk in self.chunks:
            _chunks.append(Coordinate(x=chunk.x + x, y=chunk.y + y, z=chunk.z + z))
        return Town(chunks=_chunks)

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

    def offset_towns(self, x, y, z):
        _towns = []
        for town in self.towns:
            _towns.append(town.offset_chunks(x, y, z))
        return Map(_towns)

    def get_normalised_map(self):

        offset_x = self.get_polygon_top_left_corner().x - (Chunk.SIZE / 2)
        offset_z = self.get_polygon_top_left_corner().z - (Chunk.SIZE / 2)
        return self.offset_towns(-offset_x, 0, -offset_z)

    def get_town_polygons(self) -> [Polygon]:
        """
        Returns the polygons for each town.

        If normalised is set to True, the polygons are coordinates are offset to positive integers only, as
        the polygon drawing library does not support negative coordinates.
        :return:
        """
        return [
            polygon
            for multi_polygon in self.towns
            for polygon in multi_polygon.as_polygon().geoms
        ]

    def offset_map(self, offset_x, offset_z):
        polygons = [
            polygon
            for multi_polygon in self.towns
            for polygon in multi_polygon.as_polygon().geoms
        ]
        return Map([offset_polygon(offset_x, offset_z, p) for p in polygons])

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


def offset_polygon(offset_x, offset_y, polygon):
    return Polygon([(x + offset_x, y + offset_y) for x, y in polygon.exterior.coords])


def build_town(town_name: str) -> Town:
    town = orm.unpack_town_coordinates(common.download_town(town_name))
    return Town([Chunk(x, 0, z) for x, z in town[0]])


def build_map(town_names: [str]) -> Map:
    return Map([build_town(town) for town in town_names])


def build_image_with_map(map_obj: Map) -> PIL.Image:
    """
    Prepares the map object, aligns polygons as needed, downloads images, and overlays polygons ontop. Lots going on.
    TODO refactor this
    :param map_obj: a map object
    :return: a PIL image object with the polygon overlayed ontop of the background
    """
    map_regions = list(map_obj.get_regions())

    normalised_map = map_obj.get_normalised_map()
    offset = map_obj.get_region_offset()
    map_multipolygon: Map = normalised_map.offset_towns(offset[0], 0, offset[1])

    image_data = dl.download_map_images_as_dict(map_regions)

    image: PIL.Image = img.make_image_collage(image_data)

    for map_polygon in map_multipolygon.get_town_polygons():
        image = img.make_grids_on_collage(map_polygon, image)

    return image


def resize_image(image):
    width, height = image.size
    return image.resize((width * 4, height * 4), PIL.Image.NEAREST)


def crop_image(image: PIL.Image, top_left, bottom_right):
    crop = (
        top_left.x,
        top_left.z,
        bottom_right.x + (Chunk.SIZE * 2),
        bottom_right.z + (Chunk.SIZE * 2),
    )
    return image.crop(crop)
