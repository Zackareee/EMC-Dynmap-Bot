from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union


class ColorPolygon:
    """A Polygon with an additional color attribute."""

    def __init__(self, *args, **kwargs):
        self._polygon = Polygon(*args, **kwargs)
        self._color = None  # Store color internally as an RGB tuple

    def __getattr__(self, name):
        """Delegate attribute access to the internal Polygon object."""
        return getattr(self._polygon, name)

    def __setattr__(self, name, value):
        if name == "color":
            # Expect a 6-character hex string (e.g., "ff5733") and convert to RGB
            self._color = value
        elif name == "_color" or name == "_polygon":
            super().__setattr__(name, value)
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object does not support attribute assignment for '{name}'")

    @property
    def color(self):
        """Return the stored color as an RGB tuple."""
        return self._color


class ColorMultiPolygon:
    """A container class that holds multiple ColorPolygon objects."""

    def __init__(self, colored_polygons):
        if not all(isinstance(p, ColorPolygon) for p in colored_polygons):
            raise TypeError("All elements of ColorMultiPolygon must be instances of ColorPolygon")

        self._colored_polygons = colored_polygons  # Preserve ColorPolygon instances

    def __getitem__(self, index):
        """Allow indexing like a list to get individual ColorPolygon instances."""
        return self._colored_polygons[index]

    def __iter__(self):
        """Allow iteration over the ColorPolygons."""
        return iter(self._colored_polygons)

    def __len__(self):
        """Return the number of ColorPolygons stored."""
        return len(self._colored_polygons)

    @property
    def geoms(self):
        """Return the stored ColorPolygon instances."""
        return self._colored_polygons

    def add(self, color_polygon):
        """Add a new ColorPolygon to the collection."""
        if not isinstance(color_polygon, ColorPolygon):
            raise TypeError("Only ColorPolygon instances can be added to ColorMultiPolygon")
        self._colored_polygons.append(color_polygon)


from shapely.ops import unary_union


def colored_unary_union(colored_polygons):
    """Wrapper for unary_union that returns a ColorPolygon or ColorMultiPolygon while preserving colors."""
    if not colored_polygons:
        return None  # If input list is empty, return None

    # Extract raw Shapely polygons
    polygons = [cp._polygon for cp in colored_polygons]

    # Perform unary union
    result = unary_union(polygons)

    # If the result is a single Polygon, return a ColorPolygon with the first color
    if isinstance(result, Polygon):
        colored_result = ColorPolygon(result.exterior.coords)
        colored_result.color = colored_polygons[0].color  # Use first polygon's color
        return colored_result

    # If the result is a MultiPolygon, reconstruct a ColorMultiPolygon with correct colors
    elif isinstance(result, MultiPolygon):
        new_colored_polygons = []
        for sub_polygon in result.geoms:
            # Find the original color from the input polygons (naive approach: first matching polygon)
            matching_color = next((cp.color for cp in colored_polygons if
                                   cp._polygon.contains(sub_polygon) or cp._polygon.equals(sub_polygon)), None)

            # Create a new ColorPolygon with the original color
            colored_sub_polygon = ColorPolygon(sub_polygon.exterior.coords)
            colored_sub_polygon.color = matching_color
            new_colored_polygons.append(colored_sub_polygon)

        return ColorMultiPolygon(new_colored_polygons)

    else:
        raise TypeError("Unexpected result from unary_union")
