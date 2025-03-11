from PIL import ImageChops
from dynmap_bot_core.download import common
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

    def download_map_image(self, x: int, z: int):
        return Image.open(
            f"{os.path.dirname(os.path.realpath(__file__))}/images/{x}_{z}.png"
        )

    def download_town(self, town_name):
        with open(
            f"{os.path.dirname(os.path.realpath(__file__))}/json/town/{common.sanitize_filename(town_name)}.json"
        ) as f:
            return json.load(f)[0]

    def download_nation(self, nation_name):
        with io.open(
            f"{os.path.dirname(os.path.realpath(__file__))}/json/nation/{common.sanitize_filename(nation_name)}.json",
            mode="r",
            encoding="utf-8",
        ) as f:
            return json.load(f)[0]

    @pytest.fixture(autouse=True)
    def mocked_downloads(self):
        with patch(
            "dynmap_bot_core.download.download.download_map_image",
            side_effect=self.download_map_image,
        ) as mock_map, patch(
            "dynmap_bot_core.download.common.download_town",
            side_effect=self.download_town,
        ) as mock_town, patch(
            "dynmap_bot_core.download.common.download_nation",
            side_effect=self.download_nation,
        ) as mock_nation:
            yield {
                "download_map_image": mock_map,
                "download_town": mock_town,
                "download_nation": mock_nation,
            }


