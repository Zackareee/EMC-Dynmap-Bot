__all__ = ["build_map", "build_towns", "build_map_image"]
from dynmap_bot_core.models.spatial.town import Town
from dynmap_bot_core.models.spatial.map import Map
from dynmap_bot_core.models.spatial.chunk import Chunk
from dynmap_bot_core.models.spatial.nation import Nation
from dynmap_bot_core.models.spatial.coordinate import Coordinate
from dynmap_bot_core.services import download
from dynmap_bot_core.utils import image, misc

from PIL import Image


def build_towns(town_names: [str]) -> [Town]:
    """
    Returns a town object given the town name.
    :param town_names: a list of town names
    :return:
    """
    towns_json = download.download_towns(town_names)
    result = []
    nations = set()

    for t in towns_json:
        coordinates = misc.unpack_town_coordinates(t)
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
    :param nation_names: a list of nation names
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


def build_map_image(map_obj: Map) -> Image:
    """
    Prepares the map object, aligns polygons as needed, downloads images, and overlays polygons ontop. Lots going on.
    :param map_obj: a map object
    :return: an Image object with the polygon overlayed ontop of the background
    """
    offset = map_obj.get_region_offset()
    map_regions: list[Coordinate] = list(map_obj.get_regions())
    map_obj.normalise()
    map_obj.offset_towns(-Chunk.SIZE, 0, -Chunk.SIZE)
    map_obj.offset_towns(offset[0], 0, offset[1])
    image_data = download.map_images_as_dict(map_regions)
    map_image: Image = image.stitch_images(image_data)

    map_image = image.draw_polygons_on_image(map_obj.get_town_polygons(), map_image)

    return map_image
