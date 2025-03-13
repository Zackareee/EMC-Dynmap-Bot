__all__ = ["ColorPolygon", "ColorMultiPolygon", "colored_unary_union"]
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union


class ColorPolygon:
    """A Polygon with an additional color attribute."""

    def __init__(self, color: str, *args, **kwargs) -> None:
        self._polygon: Polygon = Polygon(*args, **kwargs)
        self._color: str = color  # Store color internally as an RGB tuple

    def __getattr__(self, name) -> any:
        """Delegate attribute access to the internal Polygon object."""
        return getattr(self._polygon, name)

    def __setattr__(self, name, value) -> None:
        if name == "color":
            # Expect a 6-character hex string (e.g., "ff5733") and convert to RGB
            self._color = value
        elif name == "_color" or name == "_polygon":
            super().__setattr__(name, value)
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object does not support attribute assignment for '{name}'"
            )

    @property
    def color(self) -> str:
        """Return the stored color as an RGB tuple."""
        return self._color

    def points(self) -> list[tuple[int, int]]:
        """Returns the exterior coordinates of the polygon with an offset of 8 applied."""
        return [(int(x) + 8, int(z) + 8) for x, z in self._polygon.exterior.coords]


class ColorMultiPolygon:
    """A container class that holds multiple ColorPolygon objects."""

    def __init__(self, colored_polygons: [ColorPolygon]) -> None:
        if not all(isinstance(p, ColorPolygon) for p in colored_polygons):
            raise TypeError("All elements of ColorMultiPolygon must be instances of ColorPolygon")

        self._colored_polygons = colored_polygons  # Preserve ColorPolygon instances

    def __getitem__(self, index: int) -> ColorPolygon:
        """Allow indexing like a list to get individual ColorPolygon instances."""
        return self._colored_polygons[index]

    def __iter__(self) -> list[ColorPolygon]:
        """Allow iteration over the ColorPolygons."""
        return iter(self._colored_polygons)

    def __len__(self) -> int:
        """Return the number of ColorPolygons stored."""
        return len(self._colored_polygons)

    @property
    def geoms(self) -> list[ColorPolygon]:
        """Return the stored ColorPolygon instances."""
        return self._colored_polygons

    def add(self, color_polygon: ColorPolygon) -> None:
        """Add a new ColorPolygon to the collection."""
        if not isinstance(color_polygon, ColorPolygon):
            raise TypeError("Only ColorPolygon instances can be added to ColorMultiPolygon")
        self._colored_polygons.append(color_polygon)


def colored_unary_union(
    colored_polygons: list[ColorPolygon],
) -> ColorMultiPolygon:
    """
    Wrapper for unary_union that always returns a ColorMultiPolygon while preserving colors.
    This takes a list of ColorPolygons, combines all overlapping polygons into the fewest amount of polygons and returns
    the list of ColorMultiPolygons.
    If a single polygon remains after combining all polygons, it will still be returned as a ColorMultiPolygon
    containing a single ColorPolygon

    :param colored_polygons: A list of ColorPolygons to combine
    :return:
    """

    polygons: list[Polygon] = [cp._polygon for cp in colored_polygons]
    result: Polygon | MultiPolygon = unary_union(polygons)

    new_colored_polygons: list[ColorPolygon] = []

    if isinstance(result, Polygon):
        colored_sub_polygon: ColorPolygon = ColorPolygon(
            colored_polygons[0].color,
            result.exterior.coords,
        )
        new_colored_polygons.append(colored_sub_polygon)

    elif isinstance(result, MultiPolygon):
        for sub_polygon in result.geoms:
            matching_color: str = next(
                (cp.color for cp in colored_polygons if cp._polygon.intersects(sub_polygon)),
                colored_polygons[0].color,
            )

            colored_sub_polygon: ColorPolygon = ColorPolygon(
                matching_color,
                sub_polygon.exterior.coords,
            )
            new_colored_polygons.append(colored_sub_polygon)

    else:
        raise TypeError("Unexpected result from unary_union")

    return ColorMultiPolygon(new_colored_polygons)
