from dynmap_bot_core.models.color_polygon import ColorPolygon, ColorMultiPolygon

from dynmap_bot_core.models.spatial.chunk import Chunk
from dynmap_bot_core.models.spatial.coordinate import Coordinate
from dynmap_bot_core.models.spatial.town import Town
from dynmap_bot_core.models.spatial.map import Map


class TestChunkMethods:
    def test_coordinate_initialisation(self) -> None:
        c = Chunk(1, 32, 1)

        assert isinstance(c, Chunk)

    def test_coordinate_is_multiplied(self) -> None:
        expected = Coordinate(16, 32, 16)
        coord = Chunk(1, 32, 1)

        result = coord

        assert result == expected

    def test_chunk_coordinate_is_input(self) -> None:
        expected = Coordinate(16, 32, 16)
        coord = Chunk(1, 32, 1)

        result = coord

        assert result == expected


class TestTownMethods:
    def test_coordinate_initialisation(self) -> None:
        c = Chunk(1, 32, 1)
        t = Town([c])
        assert isinstance(t, Town)

    def test_top_left_corner(self) -> None:
        expected = Coordinate(0, 0, 0)
        coord = Chunk(1, 0, 1)
        town = Town([coord])

        result = town.get_polygon_top_left_corner()

        assert result == expected

    def test_bottom_right_corner(self) -> None:
        expected = Coordinate(16, 0, 16)
        coord = Chunk(1, 0, 1)
        town = Town([coord])

        result = town.get_polygon_bottom_right_corner()

        assert result == expected

    def test_town_as_polygon(self) -> None:
        coord = Chunk(1, 0, 1)
        town = Town([coord])

        result = town.as_polygon(town.color)

        assert isinstance(result, ColorMultiPolygon)

    def test_get_regions(self) -> None:
        coord = Chunk(1, 0, 1)
        town = Town([coord])

        result = town.get_regions()

        assert isinstance(result, set)


class TestMapMethods:
    def test_map_initialisation(self) -> None:
        c = Chunk(1, 32, 1)
        t = Town([c])
        m = Map([t])

        assert isinstance(m, Map)

    def test_map_top_left_corner(self) -> None:
        coord = Chunk(1, 0, 1)
        town = Town([coord])
        _map = Map([town])
        expected = town.get_polygon_top_left_corner()

        result = _map.get_polygon_top_left_corner()

        assert result == expected

    def test_map_bottom_right_corner(self) -> None:
        coord = Chunk(1, 0, 1)
        town = Town([coord])
        _map = Map([town])
        expected = town.get_polygon_bottom_right_corner()

        result = _map.get_polygon_bottom_right_corner()

        assert result == expected

    def test_get_town_polygons(self) -> None:
        coord = Chunk(1, 0, 1)
        town = Town([coord])
        _map = Map([town])

        result = _map.get_town_polygons()

        assert isinstance(result, list)
        for i in result:
            assert isinstance(i, ColorPolygon)

    def test_get_normalised_town_polygons(self) -> None:
        coord = Chunk(1, 0, 1)
        town = Town([coord])
        map = Map([town])

        result = map.get_town_polygons()

        assert isinstance(result, list)

    def test_normalised_polygons_minimum_is_zero(
        self,
    ) -> None:
        coord = Chunk(10, 0, 10)
        town = Town([coord])
        _map = Map([town])

        _map.normalise()
        result = _map.get_polygon_top_left_corner()
        x = result.x
        z = result.z

        assert x == 0
        assert z == 0

    def test_regions_are_accurate(self) -> None:
        expected = Coordinate(0, 0, 0)
        coord = Chunk(1, 0, 1)
        town = Town([coord])
        map = Map([town])

        result = map.get_regions()

        assert result == [expected]
