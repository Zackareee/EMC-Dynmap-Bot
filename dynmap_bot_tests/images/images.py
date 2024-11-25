from dynmap_bot_core.api_hook import common
from dynmap_bot_core.engine.overlap import coordinate
from dynmap_bot_core.orm import orm
from dynmap_bot_core import download as dl

def normalise_coordinates(
    coordinates: list[list[list[int,int]]],
    min_x,
    min_z
) -> list[list[list[int,int]]]:

    for i in coordinates:
        for coord in i:
            coord[0] -= min_x
            coord[1] -= min_z
    return coordinates


def test_images():
    vladivostok = orm.unpack_town_response(common.get_town("aomi"))
    # khogno_khan = orm.unpack_town_response(common.get_town("Khogno_Khan"))
    coordinates = coordinate.get_coordinates(vladivostok)
    image_coordinates = coordinate.get_image_coordinates(coordinates)
    for i in image_coordinates:
        dl.download_map_image(i[0], i[1])
    min_x, min_z = coordinate.get_min_coordinates_2d(image_coordinates)
    min_x *= 32
    min_z *= 32
    offset_coordinates = normalise_coordinates(coordinates, min_x, min_z)
    pass