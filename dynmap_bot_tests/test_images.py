from dynmap_bot_core.engine import misc
from dynmap_bot_core.engine.map import Map
from dynmap_bot_core.images import image
from PIL import Image, ImageChops
from dynmap_bot_core.download import common
import pytest
from dynmap_bot_tests.snapshots import *
from unittest.mock import patch
from PIL import Image
import json
import io


def download_map_image(x: int, z: int):
    return Image.open(f"./dynmap_bot_tests/images/{x}_{z}.png")


def download_town(town_name):
    with open(
        f"./dynmap_bot_tests/json/town/{common.sanitize_filename(town_name)}.json"
    ) as f:
        return json.load(f)[0]


def download_nation(nation_name):
    with io.open(
        f"./dynmap_bot_tests/json/nation/{common.sanitize_filename(nation_name)}.json",
        mode="r",
        encoding="utf-8",
    ) as f:
        return json.load(f)[0]


@pytest.fixture
def mocked_downloads():
    with patch(
        "dynmap_bot_core.download.download.download_map_image",
        side_effect=download_map_image,
    ) as mock_map, patch(
        "dynmap_bot_core.download.common.download_town", side_effect=download_town
    ) as mock_town, patch(
        "dynmap_bot_core.download.common.download_nation", side_effect=download_nation
    ) as mock_nation:
        yield {
            "download_map_image": mock_map,
            "download_town": mock_town,
            "download_nation": mock_nation,
        }


@pytest.mark.parametrize(
    "town_names",
    [
        pytest.param(["Sanctuary", "Gulf_Of_Guinea"], id="Spawn towns"),
        pytest.param(["Limerick", "Paris", "Brittany"], id="England towns"),
        pytest.param(["Limerick"], id="Limerick"),
        pytest.param(["Paris", "Brittany"], id="French towns"),
    ],
)
def test_build_map_with_town_names(town_names: list[str], mocked_downloads):
    map_obj: Map = misc.build_map(town_names)
    image_obj: Image = misc.build_image_with_map(map_obj)
    cropped_image: Image = image.crop_map_and_image(map_obj, image_obj)
    resized_image = image.resize_image(cropped_image)
    reg = Image.open("./dynmap_bot_tests/snapshots/test_build_map_with_town_names.png")
    diff = ImageChops.difference(resized_image, reg)
    assert not diff.getbbox()


def test_build_map_with_nation_names(mocked_downloads) -> None:
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


def test_coordinates_with_limerick(mocked_downloads) -> None:
    town_names: list[str] = ["Limerick"]
    map_obj: Map = misc.build_map(town_names)
    image_obj: Image = misc.build_image_with_map(map_obj)

    resized_image = image.resize_image(image_obj)
    reg = Image.open("./dynmap_bot_tests/snapshots/test_coordinates_with_limerick.png")
    diff = ImageChops.difference(resized_image, reg)
    assert not diff.getbbox()
