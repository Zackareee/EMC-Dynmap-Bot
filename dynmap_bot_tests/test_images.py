from dynmap_bot_core.engine import misc
from dynmap_bot_core.engine.map import Map
from dynmap_bot_core.images import image
from PIL import Image
from dynmap_bot_tests.base import TestBase


class TestCropMapAndImage(TestBase):
    def test_crop_with_spawn_towns(self):
        expected_image = Image.open(
            f"{self.TESTDIR}/snapshots/test_crop_spawn_towns.png"
        )

        map_obj: Map = misc.build_map(town_names=["Sanctuary", "Gulf_Of_Guinea"])
        image_obj: Image = misc.build_image_with_map(map_obj)
        cropped_image: Image = image.crop_map_and_image(map_obj, image_obj)

        self.assert_images(cropped_image, expected_image)

    def test_crop_with_nation_france(self) -> None:
        expected_image = Image.open(
            f"{self.TESTDIR}/snapshots/test_crop_with_nation_france.png"
        )

        map_obj: Map = misc.build_nations(nation_names=["France"])
        image_obj: Image = misc.build_image_with_map(map_obj)
        cropped_image: Image = image.crop_map_and_image(map_obj, image_obj)
        self.assert_images(cropped_image, expected_image)

    def test_crop_with_town_on_region_border(self) -> None:
        expected_image = Image.open(
            f"{self.TESTDIR}/snapshots/test_crop_with_town_on_region_border.png"
        )

        map_obj: Map = misc.build_map(town_names=["Limerick"])
        image_obj: Image = misc.build_image_with_map(map_obj)
        cropped_image: Image = image.crop_map_and_image(map_obj, image_obj)

        self.assert_images(cropped_image, expected_image)


class TestBuildImageWithMap(TestBase):
    def test_build_map_with_spawn_towns(self):
        expected_image = Image.open(
            f"{self.TESTDIR}/snapshots/test_build_map_with_spawn_towns.png"
        )

        map_obj: Map = misc.build_map(town_names=["Sanctuary", "Gulf_Of_Guinea"])
        image_obj: Image = misc.build_image_with_map(map_obj)

        self.assert_images(image_obj, expected_image)

    def test_build_map_with_nation_france(self) -> None:
        expected_image = Image.open(
            f"{self.TESTDIR}/snapshots/test_build_map_with_nation_france.png"
        )

        map_obj: Map = misc.build_nations(nation_names=["France"])
        image_obj: Image = misc.build_image_with_map(map_obj)

        self.assert_images(image_obj, expected_image)

    def test_build_map_with_town_on_region_border(self) -> None:
        expected_image = Image.open(
            f"{self.TESTDIR}/snapshots/test_build_map_with_town_on_region_border.png"
        )

        map_obj: Map = misc.build_map(town_names=["Limerick"])
        image_obj: Image = misc.build_image_with_map(map_obj)

        self.assert_images(image_obj, expected_image)
