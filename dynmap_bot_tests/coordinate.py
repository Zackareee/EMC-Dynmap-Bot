from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry import Polygon

from dynmap_bot_core.engine import coordinate

class TestChunkMethods:
    def test_coordinate_initialisation(self) -> None:
        c = coordinate.Chunk(1, 32, 1)

        assert isinstance(c, coordinate.Chunk)

    def test_coordinate_is_multiplied(self) -> None:
        expected = coordinate.Coordinate(16, 32, 16)
        coord = coordinate.Chunk(1, 32, 1)

        result = coord

        assert result == expected

    def test_chunk_coordinate_is_input(self) -> None:
        expected = coordinate.Coordinate(16, 32, 16)
        coord = coordinate.Chunk(1, 32, 1)

        result = coord

        assert result == expected


class TestTownMethods:
    def test_coordinate_initialisation(self) -> None:
        c = coordinate.Chunk(1, 32, 1)
        t = coordinate.Town([c])
        assert isinstance(t, coordinate.Town)

    def test_top_left_corner(self) -> None:
        expected = coordinate.Coordinate(0, 0, 0)
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])

        result = town.get_polygon_top_left_corner()

        assert result == expected

    def test_bottom_right_corner(self) -> None:
        expected = coordinate.Coordinate(16, 0, 16)
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])

        result = town.get_polygon_bottom_right_corner()

        assert result == expected

    def test_town_as_polygon(self) -> None:
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])

        result = town.as_polygon()

        assert isinstance(result, MultiPolygon)

    def test_get_regions(self) -> None:
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])

        result = town.get_regions()

        assert isinstance(result, set)


class TestMapMethods:
    def test_map_initialisation(self) -> None:
        c = coordinate.Chunk(1, 32, 1)
        t = coordinate.Town([c])
        m = coordinate.Map([t])

        assert isinstance(m, coordinate.Map)

    def test_map_top_left_corner(self) -> None:
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])
        map = coordinate.Map([town])
        expected = town.get_polygon_top_left_corner()

        result = map.get_polygon_top_left_corner()

        assert result == expected

    def test_map_bottom_right_corner(self) -> None:
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])
        map = coordinate.Map([town])
        expected = town.get_polygon_bottom_right_corner()

        result = map.get_polygon_bottom_right_corner()

        assert result == expected

    def test_get_town_polygons(self) -> None:
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])
        map = coordinate.Map([town])

        result = map.get_town_polygons()

        assert isinstance(result, list)
        for i in result:
            assert isinstance(i, Polygon)

    def test_get_normalised_town_polygons(self) -> None:
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])
        map = coordinate.Map([town])

        result = map.get_town_polygons()

        assert isinstance(result, list)

    def test_normalised_polygons_minimum_is_zero(self) -> None:
        coord = coordinate.Chunk(10, 0, 10)
        town = coordinate.Town([coord])
        map = coordinate.Map([town])

        normalised_map = map.get_normalised_map()
        result = normalised_map.get_polygon_top_left_corner()
        x = result.x
        z = result.z

        assert x == 0
        assert z == 0

    def test_regions_are_accurate(self) -> None:
        expected = coordinate.Coordinate(0, 0, 0)
        coord = coordinate.Chunk(1, 0, 1)
        town = coordinate.Town([coord])
        map = coordinate.Map([town])

        result = map.get_regions()

        assert result == [expected]
