from dynmap_bot_core.engine import misc
from dynmap_bot_core.engine.map import Map
from dynmap_bot_core.images import image
from PIL import Image
import pytest


# TODO mock these with static towns and/or json data.
# This currently just acts an an entry point to manually test.
@pytest.mark.parametrize(
    "town_names",
    [
        pytest.param(["Sanctuary", "Gulf_Of_Guinea"], id="Spawn towns"),
        pytest.param(["Limerick", "Paris", "Brittany"], id="England towns"),
        pytest.param(["Limerick"], id="Limerick"),
        pytest.param(["Paris", "Brittany"], id="French towns"),
    ],
)
def test_build_map_with_town_names(town_names: list[str]):
    map_obj: Map = misc.build_map(town_names)
    image_obj: Image = misc.build_image_with_map(map_obj)
    cropped_image: Image = image.crop_map_and_image(map_obj, image_obj)
    image.resize_image(cropped_image).show()

def test_build_map_with_nation_names():
    map_obj: Map = misc.build_nation("France")
    image_obj: Image = misc.build_image_with_map(map_obj)
    cropped_image: Image = image.crop_map_and_image(map_obj, image_obj)
    image.resize_image(cropped_image).show()

