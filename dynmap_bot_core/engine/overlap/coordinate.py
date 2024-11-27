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

def get_max_coordinates_3d(
    coordinates: list[list[list[int, int]]],
) -> tuple[int, int]:

    x_set: set = set()
    z_set: set = set()
    for i in coordinates:
        for coord in i:
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



def normalise_coordinates(
    coordinates: list[list[list[int, int]]], min_x, min_z
) -> list[list[list[int, int]]]:
    if not min_x and not min_z:
        min_x, min_z = get_min_coordinates_3d(coordinates)
    for i in coordinates:
        for coord in i:
            coord[0] -= min_x
            coord[1] -= min_z
    return coordinates


def get_coordinates(*args: town.Town) -> list[list[coordinate.Coordinate]]:
    return [i.coordinates for i in args]


def get_image_coordinates(
    coordinates: list[list[coordinate.Coordinate]],
) -> set[list[coordinate.Coordinate]]:
    image_coordinates: set[list[coordinate.Coordinate]] = set()

    for i in coordinates:
        for coord in i:
            image_coordinates.add(
                (math.floor(coord[0] / 32), math.floor(coord[1] / 32))
            )
    return list(image_coordinates)


def sort_perimeter_clockwise(perimeter_points):
    # Calculate the centroid of the points
    centroid_x = sum(x for x, y in perimeter_points) / len(perimeter_points)
    centroid_y = sum(y for x, y in perimeter_points) / len(perimeter_points)

    # Sort points by angle relative to the centroid
    def angle_from_centroid(point):
        x, y = point
        return math.atan2(y - centroid_y, x - centroid_x)

    sorted_points = sorted(perimeter_points, key=angle_from_centroid)
    return sorted_points


def calculate_perimeter(town_blocks):
    # Get the unique points from townBlocks
    points = set(map(tuple, town_blocks))

    # Define the neighbors relative to any given point
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Store the perimeter as a set of unique edges
    perimeter_edges = set()

    for x, y in points:
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            # If the neighbor is not part of the townBlocks, add the edge to the perimeter
            if neighbor not in points:
                edge = tuple(sorted([(x, y), neighbor]))
                perimeter_edges.add(edge)

    # Extract the perimeter points from the edges
    perimeter_points = {pt for edge in perimeter_edges for pt in edge}

    # Sort points clockwise
    sorted_perimeter = sort_perimeter_clockwise(list(perimeter_points))
    return sorted_perimeter


from collections import defaultdict


def reorder_cyclic_list(pairs):
    # Normalize pairs into consistent direction
    next_map = {}
    prev_map = {}

    for a, b in pairs:
        if a not in next_map and b not in prev_map:
            next_map[a] = b
            prev_map[b] = a
        elif b not in next_map and a not in prev_map:
            next_map[b] = a
            prev_map[a] = b

    # Pick an arbitrary starting point
    start = pairs[0][0]

    # Reconstruct the ordered cycle
    ordered_list = []
    current = start
    visited = set()

    while current not in visited:
        visited.add(current)
        next_node = next_map.get(current)
        if not next_node:
            raise ValueError(f"Broken link detected at {current}")
        ordered_list.append((current, next_node))
        current = next_node

    return ordered_list