__all__ = ["normalise_coordinates"]
from dynmap_bot_core.api_hook import common
from dynmap_bot_core.models import town, coordinate
from dynmap_bot_core.engine.overlap import town as ot
import math

def get_min_coordinates_3d(
    coordinates: list[list[list[int, int]]],
) -> tuple[int, int]:

    x_set: set = set()
    z_set: set = set()
    for i in coordinates:
        for coord in i:
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


def normalise_coordinates(
    coordinates: list[list[coordinate.Coordinate]],
) -> list[list[coordinate.Coordinate]]:

    min_x, min_z = get_min_coordinates_3d(coordinates)
    for i in coordinates:
        for coord in i:
            coord[0] -= min_x
            coord[1] -= min_z
    return coordinates

def get_coordinates(*args: town.Town) -> list[list[coordinate.Coordinate]]:
    return [i.coordinates for i in args]

def get_image_coordinates(coordinates: list[list[coordinate.Coordinate]]) -> set[list[coordinate.Coordinate]]:
    image_coordinates: set[list[coordinate.Coordinate]] = set()

    for i in coordinates:
        for coord in i:
            image_coordinates.add((math.floor(coord[0]/32),math.floor(coord[1]/32)))
    return list(image_coordinates)
