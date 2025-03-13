__all__ = ["Map"]
from dynmap_bot_core.engine.coordinate import Coordinate
from dynmap_bot_core.engine.town import Town
from dynmap_bot_core.engine.chunk import Chunk
from dynmap_bot_core.engine.colorpolygon import ColorMultiPolygon


class Map:
    """
    A map is a collection of Towns.
    """

    def __init__(self, towns):
        self.towns: [Town] = towns

    def get_polygon_top_left_corner(self) -> Coordinate:
        """
        Gets the upper left most coordinate of the map.
        :return:
        """
        return Coordinate(
            x=min(t.get_polygon_top_left_corner().x for t in self.towns),
            y=0,
            z=min(t.get_polygon_top_left_corner().z for t in self.towns),
        )

    def get_polygon_bottom_right_corner(self) -> Coordinate:
        """
        Gets the bottom right most coordinate of the map.
        :return:
        """
        return Coordinate(
            x=max(t.get_polygon_bottom_right_corner().x for t in self.towns),
            y=0,
            z=max(t.get_polygon_bottom_right_corner().z for t in self.towns),
        )

    def offset_towns(self, x, y, z) -> None:
        """
        Offsets all towns within the map by given x, y, z factors.
        :return: Returns a new Map object.
        """
        _towns = []
        for town in self.towns:
            town.offset_chunks(x, y, z)

    def normalise(self) -> None:
        """
        Shifts all towns on the map, such that the top left most coordinate of the Towns are now (0, 0)
        This is necessary for PIL to paste the polygons in the bounds of an image.
        :return:
        """
        offset_x = self.get_polygon_top_left_corner().x
        offset_z = self.get_polygon_top_left_corner().z
        return self.offset_towns(-offset_x, 0, -offset_z)

    def get_town_polygons(self) -> list[ColorMultiPolygon]:
        """
        Returns the polygons for each town.
        :return:
        """
        map_polygons: list[ColorMultiPolygon] = []
        for town in self.towns:
            town_polygons: ColorMultiPolygon = town.as_polygon(color=f"#{town.color}").geoms
            map_polygons += town_polygons
        return map_polygons

    def get_region_offset(self) -> list[int]:
        """
        Gets the maps offset from the nearest region border
        """
        minimum_coordinate: Coordinate = self.get_polygon_top_left_corner()
        x_offset: int = (minimum_coordinate.x + Chunk.SIZE) % 512
        z_offset: int = (minimum_coordinate.z + Chunk.SIZE) % 512
        offset: list[int] = [x_offset, z_offset]
        return offset

    def get_regions(self) -> list[Coordinate]:
        """
        Gets all unique regions the Map is within as Coordinates.
        :return:
        """
        regions = set()
        for town in self.towns:
            towns_regions: set[Coordinate] = town.get_regions()
            [regions.add(coord) for coord in towns_regions]
        return list(regions)
