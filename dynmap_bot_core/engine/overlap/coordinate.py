__all__ = ["multiply_coordinates"]

from itertools import chain
import math
from dynmap_bot_core.orm import orm
from shapely.geometry.base import BaseGeometry
from dynmap_bot_core.images import image as img
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union
from abc import ABC, abstractmethod


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

    def get_coordinates(self):
        pass

    def get_chunk(self) -> [int]:
        pass

    def get_region(self) -> [int]:
        pass

class Coordinate(Location):
    def get_coordinates(self) -> [float]:
        return [self.x, self.y, self.z]

    def get_chunk(self) -> [int]:
        return [round(self.x / 16), round(self.z / 16)]

    def get_region(self) -> [int]:
        return [round(self.x / 512), round(self.z / 512)]

class Chunk(Location):
    def get_coordinates(self) -> [float]:
        return [self.x * 16, self.y, self.z * 16]

    def get_chunk(self) -> [int]:
        return [self.x, self.z]

    def get_region(self) -> [int]:
        return [round(self.x / 32), round(self.z / 32)]


class Town:
    def __init__(self, coordinates):
        self.coordinates: [Coordinate] = coordinates

    def get_town(self):
        squares: [Polygon] = []
        for coordinate in self.coordinates:
            x, y, z = coordinate.get_coordinates()
            squares.append(Polygon([
            (x - 8, z - 8),
            (x - 8, z + 8),
            (x + 8, z + 8),
            (x + 8, z - 8),
        ]))
        merged_polygon = unary_union(squares)
        return merged_polygon

    def get_regions(self) -> list[int, int]:
        regions = set()
        for coordinate in self.coordinates:
            regions.add(tuple(coordinate.get_region()))
        return list(regions)

class Map:
    def __init__(self, towns):
        self.towns: [Town] = towns

    def get_map(self) -> [Polygon]:
        polygons = [i.get_town() for i in self.towns]
        return polygons

    def get_normalized_map(self):
        merged_map = unary_union(self.get_map())
        multipolygon: MultiPolygon = ensure_multipolygon(merged_map)
        min_x = min(coord[0] for polygon in multipolygon.geoms for coord in polygon.exterior.coords) * -1
        min_z = min(coord[1] for polygon in multipolygon.geoms for coord in polygon.exterior.coords) * -1

        normalised_polygon = []
        for town in self.get_map():
            town = Polygon([(x + min_x, y + min_z) for x, y in town.exterior.coords])
            normalised_polygon.append(town)

        return normalised_polygon

    def get_offset_map(self, offset_x, offset_z):
        normalized_map = self.get_normalized_map()
        offset_map = []
        for town in normalized_map:
            town = Polygon([(x + offset_x, y + offset_z) for x, y in town.exterior.coords])
            offset_map.append(town)

        return offset_map

    def get_regions(self) -> [[int,int]]:
        regions = set()
        for town in self.towns:
            [regions.add(i) for i in town.get_regions()]
        return list(regions)

# def a_crude_ass_way_of_collating_perimeters(grid_points: list[list[int, int]]):
#     boundaries = []
#     squares = [Polygon([
#         (x - 8, y - 8),
#         (x - 8, y + 8),
#         (x + 8, y + 8),
#         (x + 8, y - 8),
#     ]) for x, y in grid_points]
#     merged_polygon = unary_union(squares)
#     if merged_polygon.geom_type == 'MultiPolygon':
#         for i in merged_polygon.geoms:
#             boundaries.append(list(i.exterior.coords))
#     else:
#         boundaries = [list(merged_polygon.exterior.coords)]
#     # Extract the boundary (external edges) of the merged geometry
#     return boundaries



def get_min_coordinates_3d(
    coordinates: list[list[list[int, int]]],
) -> tuple[int, int]:

    x_set: set = set()
    z_set: set = set()
    for coord in coordinates:
        x_set.add(coord[0])
        z_set.add(coord[1])

    min_x = min(x_set)
    min_z = min(z_set)

    return min_x, min_z

def get_min_coordinates_2d(
    coordinates: list[list[int, int]],
) -> tuple[int, int]:

    x_set: set = set()
    z_set: set = set()
    for coord in coordinates:
        x_set.add(coord[0])
        z_set.add(coord[1])

    min_x = min(x_set)
    min_z = min(z_set)

    return min_x, min_z

def normalise_coordinates(coordinates: list[list[int]], min_x, min_z ) -> list[list[int]]:
    return [[x - min_x, z - min_z] for x, z in coordinates]

def multiply_coordinates(coordinates: list[list[int]], factor: int = 16 ) -> list[list[int]]:
    return [[x * factor, z * factor] for x, z in coordinates]


def get_chunks(*args: orm.Town) -> orm.TownCoordinates:
    coords = [i.coordinates for i in args]
    return orm.TownCoordinates(coords[0])

def get_regions_from_chunks(town_: orm.TownCoordinates):
    regions = set()
    for x, z in town_.coordinates:
        regions.add(
            (math.floor(x/32),math.floor(z/32))
        )
    return list(regions)

def towns_to_polygons(towns_: orm.TownCoordinates, regions_: list[tuple[int]]):
    all_chunks = [i.coordinates for i in towns_]
    flattened_coordinates = list(
        chain.from_iterable(item if isinstance(item, list) else [item] for item in all_chunks)
    )
    minx, minz = get_min_coordinates_2d([[x * 32, z * 32] for x, z in regions_])
    normalised_town_chunks = [normalise_coordinates(i, minx, minz) for i in all_chunks]
    multiplied_town_chunks = [multiply_coordinates(i, 16) for i in normalised_town_chunks]
    town_polygs = [img.a_crude_ass_way_of_collating_perimeters(i) for i in multiplied_town_chunks]
    return town_polygs

