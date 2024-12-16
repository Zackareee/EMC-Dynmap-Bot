from dynmap_bot_core.api_hook import common
from dynmap_bot_core.engine.overlap import coordinate
from dynmap_bot_core.orm import orm


def test_normalise_coordinates():
    vladivostok = orm.unpack_town_response(common.get_town("Vladivostok"))
    khogno_khan = orm.unpack_town_response(common.get_town("Khogno_Khan"))

    coords = coordinate.multiply_coordinates(
        coordinate.get_chunks(vladivostok, khogno_khan)
    )
