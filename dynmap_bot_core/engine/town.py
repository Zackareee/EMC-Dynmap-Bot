__all__ = ["Town"]

from shapely.geometry.polygon import Polygon

from dynmap_bot_core.engine.chunk import Chunk
from dynmap_bot_core.engine.coordinate import Coordinate
from dynmap_bot_core.download import common
from shapely.geometry import MultiPolygon
from shapely.ops import unary_union
from PIL import ImageColor
from dynmap_bot_core.engine.colored_polygon import ColoredPolygon


def hex_to_rgba(hex_color: str) -> tuple:
    rgb_color = ImageColor.getcolor(f"#{hex_color}", "RGB")
    rgba_color = rgb_color + (100,)
    return rgba_color


def unpack_town_color(town_json: dict) -> tuple[int, ...]:
    """
    Given a dictionary of a town object, return all coordinates
    :param town_json: Town object as a dictionary.
    :return: list of ints for all coordinates.
    """
    nation_name: str = town_json["nation"]["name"]
    if nation_name is not None:
        nation = common.download_nation(nation_name)
        hex_color = nation["dynmapColour"]
    else:
        hex_color = "89c500"
    return hex_to_rgba(hex_color)


def ensure_multipolygon(geometry: ColoredPolygon | MultiPolygon) -> MultiPolygon:
    """
     Convert a Polygon to a MultiPolygon if it isn't one already.
    :param geometry: A possible Polygon or Multipolygon.
    :return:
    """
    if isinstance(geometry, Polygon):
        return MultiPolygon([geometry])
    elif isinstance(geometry, MultiPolygon):
        return geometry
    else:
        raise TypeError("Input geometry must be a Polygon or MultiPolygon.")


class Town:
    def __init__(
        self,
        town_name: str,
        chunks: list[Coordinate] | None = None,
        colour: tuple[int, int, int, int] = None,
    ):
        self.town_name = town_name
        self.chunks: [Coordinate] = chunks
        self.colour = colour
        self._init()

    def _init(self):
        if self.colour is None:
            self.colour = unpack_town_color(common.download_town(self.town_name))
        if self.chunks is None:
            self.chunks = self._build_town()

    def _build_town(self):
        """
        Returns a town object given the town name.
        :param town_name:
        :return:
        """
        town_json = common.download_town(self.town_name)
        town_coordinates: list[list[int, int]] = [
            town_json["coordinates"]["townBlocks"]
        ]
        return [Chunk(x, 0, z) for x, z in town_coordinates[0]]

    def offset_chunks(self, x, y, z) -> "Town":
        """
        Offsets all chunks within a town by given x, y, z factors.
        :return: Returns a new Town object.
        """
        _chunks = []
        for chunk in self.chunks:
            _chunks.append(Coordinate(x=chunk.x + x, y=chunk.y + y, z=chunk.z + z))
        return Town(town_name=self.town_name, chunks=_chunks, colour=self.colour)

    def get_polygon_top_left_corner(self) -> Coordinate:
        """
        Helper function to get the upper left most Coordinate of a town, useful for minimum coordinates of a town.
        Coordinate location may not necessarily within the bounds of the town, but instead representative of its upper
        left most corner.
        :return:
        """
        padding: int = Chunk.SIZE
        return Coordinate(
            x=min(c.x for c in self.chunks) - padding,
            y=0,
            z=min(c.z for c in self.chunks) - padding,
        )

    def get_polygon_bottom_right_corner(self) -> Coordinate:
        """
        Helper function to get the bottom right most corner, useful for maximum coordinates of a town.
        Coordinate location may not necessarily within the bounds of the town, but instead representative of its bottom
        right most corner.
        :return:
        """
        return Coordinate(
            x=max(c.x for c in self.chunks), y=0, z=max(c.z for c in self.chunks)
        )

    def as_polygon(self) -> MultiPolygon:
        """
        Returns the town as a MultiPolygon object where the bounds of the polygon(s) are the border(s) of the town.
        :return:
        """
        padding = Chunk.SIZE / 2
        unary_polygon = unary_union(
            [
                Polygon(
                    [
                        (c.x - padding, c.z - padding),
                        (c.x - padding, c.z + padding),
                        (c.x + padding, c.z + padding),
                        (c.x + padding, c.z - padding),
                    ]
                )
                for c in self.chunks
            ]
        )
        return ensure_multipolygon(unary_polygon)

    def get_regions(self) -> set[Coordinate]:
        """
        Gets all unique regions the Town is within as Coordinates.
        """
        # To account for regions that are non-rectangular shaped,
        # dedupe all the regions for all included chunks.
        return set(chunk.get_region_coordinate() for chunk in self.chunks)
