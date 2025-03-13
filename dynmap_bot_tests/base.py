from PIL import ImageChops
from dynmap_bot_core.utils import misc
from dynmap_bot_core.models.spatial.coordinate import Coordinate
import pytest
from unittest.mock import patch
from PIL import Image
import json
import io
import os
import numpy as np


class TestBase:
    """Base test class that provides common assertions."""

    TESTDIR = os.path.dirname(os.path.realpath(__file__))

    def assert_images(self, cropped_image, expected_image):
        """Assert that two images are identical."""
        diff = ImageChops.difference(cropped_image, expected_image)
        diff_array = np.array(diff)
        assert np.all(diff_array == 0), "Images do not match!"

    def download_map_image(self, coord: Coordinate):
        return Image.open(f"{os.path.dirname(os.path.realpath(__file__))}/images/{coord.x}_{coord.z}.png")

    def download_town(self, town_names: list[str]):
        result = []
        for town in town_names:
            with open(
                f"{os.path.dirname(os.path.realpath(__file__))}/json/town/{misc.sanitize_filename(town)}.json"
            ) as f:
                result.append(json.load(f)[0])
        return result

    def download_nation(self, nation_names):
        result = []
        for nation in nation_names:
            with io.open(
                f"{os.path.dirname(os.path.realpath(__file__))}/json/nation/{misc.sanitize_filename(nation)}.json",
                mode="r",
                encoding="utf-8",
            ) as f:
                result.append(json.load(f)[0])
        return result

    @pytest.fixture(autouse=True)
    def mocked_downloads(self):
        with patch(
            "dynmap_bot_core.services.download.download_map_image",
            side_effect=self.download_map_image,
        ) as mock_map, patch(
            "dynmap_bot_core.services.download.download_towns",
            side_effect=self.download_town,
        ) as mock_town, patch(
            "dynmap_bot_core.services.download.download_nations",
            side_effect=self.download_nation,
        ) as mock_nation:
            yield {
                "download_map_image": mock_map,
                "download_towns": mock_town,
                "download_nations": mock_nation,
            }
