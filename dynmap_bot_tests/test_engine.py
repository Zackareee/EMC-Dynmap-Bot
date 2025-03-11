from dynmap_bot_core.engine import misc
from dynmap_bot_core.engine.map import Map
from dynmap_bot_core.engine.town import Town

from dynmap_bot_tests.base import TestBase

class TestBuildMap(TestBase):
    def test_build_map_returns_map_instance(self):
        town_names = ["Sanctuary", "Gulf_Of_Guinea"]

        map_obj: Map = misc.build_map(town_names=town_names)

        assert isinstance(map_obj, Map)

    def test_build_map_returns_map_instance_with_correct_length(self):
        town_names = ["Sanctuary", "Gulf_Of_Guinea"]

        map_obj: Map = misc.build_map(town_names=town_names)

        assert len(map_obj.towns) == 2

    def test_build_map_contains_towns(self):
        town_names = ["Sanctuary", "Gulf_Of_Guinea"]

        map_obj: Map = misc.build_map(town_names=town_names)

        for town in map_obj.towns:
            assert isinstance(town, Town)


    def test_get_regions(self):
        map_obj: Map = misc.build_map(town_names=["Sanctuary", "Gulf_Of_Guinea"])

        result = map_obj.get_regions()

        assert isinstance(result, list)
        assert len(result) == 4
