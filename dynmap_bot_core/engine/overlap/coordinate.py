__all__ = ["normalise_coordinates"]
from dynmap_bot_core.api_hook import common
from dynmap_bot_core.models import town, coordinate
from dynmap_bot_core.engine.overlap import town as ot


def _get_min_coordinates(
    coordinates: list[list[coordinate.Coordinate]],
) -> tuple[int, int]:

    x_set: set = set()
    z_set: set = set()
    for i in coordinates:
        for coord in i:
            x_set.add(coord.x)
            z_set.add(coord.z)

    min_x = min(x_set)
    min_z = min(z_set)

    return min_x, min_z


def normalise_coordinates(
    coordinates: list[list[coordinate.Coordinate]],
) -> list[list[coordinate.Coordinate]]:

    min_x, min_z = _get_min_coordinates(coordinates)
    for i in coordinates:
        for coord in i:
            coord.x -= min_x
            coord.z -= min_z
    return coordinates


all_towns = common.get_all_towns()
all_towns_obj = []
for i in all_towns[:250]:
    name = i["name"]
    town_temp = common.get_town(name)
    all_towns_obj.append(town.unpack_town_response(town_temp))

vladivostok = town.unpack_town_response(common.get_town("Vladivostok"))
khogno_khan = town.unpack_town_response(common.get_town("Khogno_Khan"))

coords = normalise_coordinates(ot.get_coordinates(vladivostok, khogno_khan))

pass
