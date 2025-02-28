from dynmap_bot_core.engine import misc
from dynmap_bot_core.engine.map import Map
from dynmap_bot_core.images import image
from PIL import Image, ImageChops
import pytest
from dynmap_bot_tests.snapshots import *


# TODO mock these with static towns and/or json data.
# This currently just acts an an entry point to manually test.
@pytest.mark.parametrize(
    "town_names",
    [
        pytest.param(["Sanctuary", "Gulf_Of_Guinea"], id="Spawn towns"),
    ],
)
def test_build_map_with_town_names(town_names: list[str]):

    map_obj: Map = misc.build_map(town_names)
    image_obj: Image = misc.build_image_with_map(map_obj)
    cropped_image: Image = image.crop_map_and_image(map_obj, image_obj)
    resized_image = image.resize_image(cropped_image)
    reg = Image.open("./dynmap_bot_tests/snapshots/test_build_map_with_town_names.png")
    diff = ImageChops.difference(resized_image, reg)
    assert not diff.getbbox()


def test_build_map_with_nation_names():
    Image.MAX_IMAGE_PIXELS = 292990976

    map_obj: Map = misc.build_nation("France")
    image_obj: Image = misc.build_image_with_map(map_obj)
    cropped_image: Image = image.crop_map_and_image(map_obj, image_obj)

    resized_image = image.resize_image(cropped_image)
    reg = Image.open(
        "./dynmap_bot_tests/snapshots/test_build_map_with_nation_names.png"
    )
    diff = ImageChops.difference(resized_image, reg)
    assert not diff.getbbox()


def test_coordinates_with_limerick():
    town_names: list[str] = ["Limerick"]
    map_obj: Map = misc.build_map(town_names)
    image_obj: Image = misc.build_image_with_map(map_obj)

    resized_image = image.resize_image(image_obj)
    reg = Image.open("./dynmap_bot_tests/snapshots/test_coordinates_with_limerick.png")
    diff = ImageChops.difference(resized_image, reg)
    assert not diff.getbbox()
