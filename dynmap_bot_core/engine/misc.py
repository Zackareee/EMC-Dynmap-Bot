__all__ = ["build_map", "build_towns", "build_image_with_map"]
from dynmap_bot_core.engine.town import Town
from dynmap_bot_core.engine.map import Map
from dynmap_bot_core.engine.chunk import Chunk
from dynmap_bot_core.engine.nation import Nation
from dynmap_bot_core.engine.coordinate import Coordinate
from dynmap_bot_core.download import download
from dynmap_bot_core.images import image as img
from PIL import Image
import urllib.parse


def sanitize_filename(filename: str) -> str:
    """
    Serves as a helper function for tests to sanitize a filename to meet the windows filename requirements.
    Use urllib.parse.unquote(str) to recover the filename.
    :param filename:
    :return:
    """
    safe_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.() "
    sanitized = urllib.parse.quote(filename, safe=safe_chars)
    sanitized = sanitized.rstrip(" .")
    return sanitized


def unpack_town_coordinates(town_json: dict) -> list[list[int, int]]:
    """
    Given a dictionary of a town object, return all coordinates
    :param town_json: Town object as a dictionary.
    :return: list of ints for all coordinates.
    """
    coordinates: list[list[int, int]] = [town_json["coordinates"]["townBlocks"]]
    return coordinates


# TODO build an abstraction on town so nations and towns can be mixed - Maybe a bad idea since a town and nation can
#  have the same name
def build_towns(town_names: [str]) -> [Town]:
    """
    Returns a town object given the town name.
    :param town_names:
    :return:
    """
    towns_json = download.download_towns(town_names)
    result = []
    nations = set()

    for t in towns_json:
        coordinates = unpack_town_coordinates(t)
        town = Town([Chunk(x, 0, z) for x, z in coordinates[0]])
        town.nation_name = t["nation"]["name"]
        if town.nation_name is not None:
            nations.add(town.nation_name)
        result.append(town)

    nations_json = download.download_nations(list(nations))
    nations_dict: dict = {nation["name"]: nation for nation in nations_json}

    for town in result:
        if town.nation_name:
            town.color = nations_dict[town.nation_name]["dynmapColour"]

    return result


def build_nations(nation_names: [str]) -> Nation:
    """
    Returns a town object given the town name.
    :param nation_name:
    :return:
    """
    nations_json = download.download_nations(nation_names)
    result = []
    for n in nations_json:
        town_names_dict = n["towns"]
        town_names = [item["name"] for item in town_names_dict]
        towns = build_towns(town_names)
        result += towns
    return Nation(result)


def build_map(town_names: list[str]) -> Map:
    """
    Returns a Map object given the town names.
    :param town_names:
    :return:
    """
    towns = build_towns(town_names)
    return Map(towns)


def build_image_with_map(map_obj: Map) -> Image:
    """
    Prepares the map object, aligns polygons as needed, downloads images, and overlays polygons ontop. Lots going on.
    TODO refactor this - the current setup will not work with nations
    :param map_obj: a map object
    :return: an Image object with the polygon overlayed ontop of the background
    """
    offset = map_obj.get_region_offset()
    map_regions: list[Coordinate] = list(map_obj.get_regions())
    map_obj.normalise()
    map_obj.offset_towns(-Chunk.SIZE, 0, -Chunk.SIZE)
    map_obj.offset_towns(offset[0], 0, offset[1])
    image_data = download.map_images_as_dict(map_regions)
    image: Image = img.make_image_collage(image_data)

    image = img.make_grids_on_collage(map_obj.get_town_polygons(), image)

    return image
