__all__ = ["multiply_coordinates"]

from itertools import chain
from dynmap_bot_core.api_hook import common
from dynmap_bot_core.models import town, coordinate
from dynmap_bot_core.engine.overlap import town as ot
import math
from dynmap_bot_core.orm import orm
from dynmap_bot_core.images import image as img

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

def get_max_coordinates_3d(
    coordinates: list[list[list[int, int]]],
) -> tuple[int, int]:

    x_set: set = set()
    z_set: set = set()
    for coord in coordinates:
        x_set.add(coord[0])
        z_set.add(coord[1])

    max_x = max(x_set)
    max_z = max(z_set)

    return max_x, max_z


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

def get_max_coordinates_2d(
    coordinates: list[list[int, int]],
) -> tuple[int, int]:

    x_set: set = set()
    z_set: set = set()
    for coord in coordinates:
        x_set.add(coord[0])
        z_set.add(coord[1])

    max_x = max(x_set)
    max_z = max(z_set)

    return max_x, max_z



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

