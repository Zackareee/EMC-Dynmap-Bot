__all__ = ["Nation"]
from dynmap_bot_core.engine.map import Map
from dynmap_bot_core.download import common
from dynmap_bot_core.engine.town import Town, hex_to_rgba


class Nation(Map):
    def __init__(self, nation_name: str):
        self.nation_name = nation_name
        self.towns: [Town] = None
        self._json = common.download_nation(self.nation_name)
        self._dynmapColor = hex_to_rgba(self._json["dynmapColour"])

        self._init()

        super().__init__(self.towns)

    def _init(self):
        self.towns = self._build_towns()

    def _build_towns(self):
        town_names_dict = self._json["towns"]
        town_names = [item["name"] for item in town_names_dict]
        towns = [Town(town_name, colour=self._dynmapColor) for town_name in town_names]
        return towns
