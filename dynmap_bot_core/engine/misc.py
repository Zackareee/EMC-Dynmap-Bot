__all__ = ["build_map", "build_image_with_map"]
from dynmap_bot_core.engine.town import Town
from dynmap_bot_core.engine.map import Map
from dynmap_bot_core.engine.coordinate import Coordinate
from dynmap_bot_core import download as dl
from dynmap_bot_core.images import image as img
from PIL import Image


def unpack_town_coordinates(town_json: dict) -> list[list[int, int]]:
    """
    Given a dictionary of a town object, return all coordinates
    :param town_json: Town object as a dictionary.
    :return: list of ints for all coordinates.
    """
    coordinates: list[list[int, int]] = [town_json["coordinates"]["townBlocks"]]
    return coordinates

def build_map(town_names: list[str]) -> Map:
    """
    Returns a Map object given the town names.
    :param town_names:
    :return:
    """
    towns = [Town(town_name) for town_name in town_names]
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

    for map_dict in map_multipolygon.get_polygons():
        image = img.make_grids_on_collage(map_dict, image)

    return image
