from dynmap_bot_core.api_hook import common
from dynmap_bot_core.models import town, coordinate

vladivostok = town.unpack_town_response(common.get_town("Vladivostok"))
khogno_khan = town.unpack_town_response(common.get_town("Khogno_Khan"))


def get_coordinates(*args: town.Town) -> list[list[coordinate.Coordinate]]:
    return [i.coordinates.townBlocks for i in args]


# coords = get_coordinates(vladivostok, khogno_khan)
# pass
