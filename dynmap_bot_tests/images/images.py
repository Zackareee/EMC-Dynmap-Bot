from numpy.random import normal
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry import Polygon

from dynmap_bot_core.api_hook import common
from dynmap_bot_core.engine.overlap import coordinate
from dynmap_bot_core.engine.overlap.coordinate import (
    build_image_with_map,
    crop_image,
    resize_image,
)
from dynmap_bot_core.orm import orm
from dynmap_bot_core import download as dl
from dynmap_bot_core.images import image as img
import PIL


def test_images():
    town_names = ["Sanctuary", "ILoveFix", "Gulf_Of_Guinea", "PearlyGates"]
    towns = [orm.unpack_town_response(common.get_town(town)) for town in town_names]

    coordinates = coordinate.get_chunks(*towns)
    image_coordinates = coordinate.get_background_image_coordinates(coordinates)
    image_data = dl.download_map_images_as_dict(image_coordinates)

    min_x, min_z = coordinate.get_min_coordinates_2d(image_coordinates)
    min_x *= 32
    min_z *= 32
    offset_coordinates = coordinate.multiply_coordinates(coordinates, min_x, min_z)
    image: PIL.Image = img.make_image_collage(offset_coordinates, image_data)
    image.save(
        r"C:\Users\zacka\Documents\Projects\EMC-Dynmap-Bot\output_collage_with_polygon.png"
    )


def test_make_square():
    img.make_square_lines([0, 0])


def test_perimeter_collapsing():
    # town_names = ["Cape_Verde"]
    town_names = ["Sanctuary", "ILoveFix", "Gulf_Of_Guinea", "PearlyGates"]

    towns = [orm.unpack_town_response(common.get_town(town)) for town in town_names]
    town_chunks = [coordinate.get_chunks(town) for town in towns]
    town_regions = [
        region
        for town in town_chunks
        for region in coordinate.get_regions_from_chunks(town)
    ]
    town_polygons = coordinate.towns_to_polygons(town_chunks, town_regions)
    image_data = dl.download_map_images_as_dict(town_regions)
    image: PIL.Image = img.make_image_collage(image_data)

    for i in town_polygons:
        image = img.make_grids_on_collage([i], image)
    width, height = image.size
    image = image.resize((width * 4, height * 4), PIL.Image.NEAREST)
    image.show()


class TestChunkMethods:
    def test_coordinate_initialisation(self) -> None:
        # town_names = ["Cape_Verde"]
        c = coordinate.Chunk(1, 32, 1)

        assert isinstance(c, coordinate.Chunk)

    def test_coordinate_is_multiplied(self) -> None:
        # town_names = ["Cape_Verde"]
        expected = coordinate.Coordinate(16, 32, 16)
        coord = coordinate.Chunk(1, 32, 1)

        result = coord

        assert result == expected

    def test_chunk_coordinate_is_input(self) -> None:
        # town_names = ["Cape_Verde"]
        expected = coordinate.Coordinate(16, 32, 16)
        coord = coordinate.Chunk(1, 32, 1)

        result = coord

        assert result == expected


class TestTownMethods:
    def test_coordinate_initialisation(self) -> None:
        # town_names = ["Cape_Verde"    ]
        c = coordinate.Chunk(1, 32, 1)
        t = coordinate.Town([c])
        assert isinstance(t, coordinate.Town)

    def test_top_left_corner(self) -> None:
        # town_names = ["Cape_Verde"]
        expected = coordinate.Coordinate(0, 0, 0)
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])

        result = town.get_polygon_top_left_corner()

        assert result == expected

    def test_bottom_right_corner(self) -> None:
        # town_names = ["Cape_Verde"]
        expected = coordinate.Coordinate(16, 0, 16)
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])

        result = town.get_polygon_bottom_right_corner()

        assert result == expected

    def test_town_as_polygon(self) -> None:
        # town_names = ["Cape_Verde"]
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])

        result = town.as_polygon()

        assert isinstance(result, MultiPolygon)

    def test_get_regions(self) -> None:
        # town_names = ["Cape_Verde"]
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])

        result = town.get_regions()

        assert isinstance(result, set)


class TestMapMethods:
    def test_map_initialisation(self) -> None:
        # town_names = ["Cape_Verde"]
        c = coordinate.Chunk(1, 32, 1)
        t = coordinate.Town([c])
        m = coordinate.Map([t])

        assert isinstance(m, coordinate.Map)

    def test_map_top_left_corner(self) -> None:
        # town_names = ["Cape_Verde"]
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])
        map = coordinate.Map([town])
        expected = town.get_polygon_top_left_corner()

        result = map.get_polygon_top_left_corner()

        assert result == expected

    def test_map_bottom_right_corner(self) -> None:
        # town_names = ["Cape_Verde"]
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])
        map = coordinate.Map([town])
        expected = town.get_polygon_bottom_right_corner()

        result = map.get_polygon_bottom_right_corner()

        assert result == expected

    def test_get_town_polygons(self) -> None:
        # town_names = ["Cape_Verde"]
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])
        map = coordinate.Map([town])

        result = map.get_town_polygons()

        assert isinstance(result, list)
        for i in result:
            assert isinstance(i, Polygon)

    def test_get_normalised_town_polygons(self) -> None:
        # town_names = ["Cape_Verde"]
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])
        map = coordinate.Map([town])

        result = map.get_town_polygons()

        assert isinstance(result, list)

    def test_normalised_polygons_minimum_is_zero(self) -> None:
        # town_names = ["Cape_Verde"]
        coord = coordinate.Chunk(10, 0, 10)
        town = coordinate.Town([coord])
        map = coordinate.Map([town])

        normalised_map = map.get_normalised_map()
        result = normalised_map.get_polygon_top_left_corner()
        x = result.x
        z = result.z

        assert x == 8
        assert z == 8

    def test_regions_are_accurate(self) -> None:
        # town_names = ["Cape_Verde"]
        expected = coordinate.Coordinate(0, 0, 0)
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])
        map = coordinate.Map([town])

        result = map.get_regions()

        assert result == [expected]


def test_coordinates_with_map():
    town_names = ["Sanctuary", "ILoveFix", "Gulf_Of_Guinea", "PearlyGates"]
    map_obj = coordinate.build_map(town_names)

    normalised_map = map_obj.get_normalised_map()
    offset = map_obj.get_region_offset()
    map_multipolygon = normalised_map.offset_towns(offset[0], 0, offset[1])

    image_obj = build_image_with_map(map_obj)
    image_obj: PIL.Image = crop_image(
        image_obj,
        map_multipolygon.get_polygon_top_left_corner(),
        map_multipolygon.get_polygon_bottom_right_corner(),
    )
    resize_image(image_obj).show()
    resize_image(image_obj).save(r"C:\Users\zacka\Documents\image.png")
