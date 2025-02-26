__all__ = ["build_map", "build_town", "build_image_with_map"]
from dynmap_bot_core.engine.town import Town
from dynmap_bot_core.engine.map import Map
from dynmap_bot_core.engine.chunk import Chunk
from dynmap_bot_core.engine.nation import Nation
from dynmap_bot_core.engine.coordinate import Coordinate
from dynmap_bot_core.download import common
from dynmap_bot_core import download as dl
from dynmap_bot_core.images import image as img
from PIL import Image, ImageColor


def unpack_town_coordinates(town_json: dict) -> list[list[int, int]]:
    """
    Given a dictionary of a town object, return all coordinates
    :param town_json: Town object as a dictionary.
    :return: list of ints for all coordinates.
    """
    coordinates: list[list[int, int]] = [town_json["coordinates"]["townBlocks"]]
    return coordinates

def unpack_town_colour(town_json: dict) -> tuple[int, ...]:
    """
    Given a dictionary of a town object, return all coordinates
    :param town_json: Town object as a dictionary.
    :return: list of ints for all coordinates.
    """
    nation_name: str = town_json["nation"]["name"]
    if nation_name is not None:
        nation = common.download_nation(nation_name)
        hex_colour = nation["dynmapColour"]
    else:
        hex_colour = "89c500"
    rgb_colour = ImageColor.getcolor(f"#{hex_colour}", "RGB")
    rgba_colour = rgb_colour + (100,)
    return rgba_colour


# TODO build an abstraction on town so nations and towns can be mixed - Maybe a bad idea since a town and nation can
#  have the same name
def build_town(town_name: str) -> Town:
    """
    Returns a town object given the town name.
    :param town_name:
    :return:
    """
    town = common.download_town(town_name)
    town_obj: list[list[int, int]] = unpack_town_coordinates(
        town
    )
    town_colour = unpack_town_colour(town)
    return Town(chunks=[Chunk(x, 0, z) for x, z in town_obj[0]], colour=town_colour)


def build_nation(nation_name: str) -> Nation:
    """
    Returns a town object given the town name.
    :param nation_name:
    :return:
    """
    town_names_dict = common.download_nation(nation_name)["towns"]
    town_names = [item["name"] for item in town_names_dict]
    towns = [build_town(town) for town in town_names]
    return Nation(towns)


def build_map(town_names: list[str]) -> Map:
    """
    Returns a Map object given the town names.
    :param town_names:
    :return:
    """
    towns = [build_town(town) for town in town_names]
    return Map(towns)


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

    for map_dict in map_multipolygon.get_town_polygons():
        image = img.make_grids_on_collage(map_dict, image)

    return image
