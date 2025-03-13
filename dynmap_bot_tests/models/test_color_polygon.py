import pytest
from shapely.geometry import Polygon
from dynmap_bot_core.models.color_polygon import (
    ColorPolygon,
    ColorMultiPolygon,
    colored_unary_union,
)


def test_instantiation():
    poly = ColorPolygon("#FFFFFF", [(0, 0), (1, 1), (1, 0)])
    assert isinstance(poly, ColorPolygon)
    assert isinstance(poly._polygon, Polygon)
    assert poly.area == Polygon([(0, 0), (1, 1), (1, 0)]).area


def test_coordinates():
    poly = ColorPolygon("#FFFFFF", [(0, 0), (1, 1), (1, 0)])
    assert list(poly.exterior.coords) == list(Polygon([(0, 0), (1, 1), (1, 0)]).exterior.coords)


def test_polygon_methods():
    poly = ColorPolygon("#FFFFFF", [(0, 0), (1, 1), (1, 0)])
    assert poly.area == Polygon([(0, 0), (1, 1), (1, 0)]).area
    assert poly.bounds == Polygon([(0, 0), (1, 1), (1, 0)]).bounds


def test_immutability():
    poly = ColorPolygon("#FFFFFF", [(0, 0), (1, 1), (1, 0)])

    with pytest.raises(AttributeError):
        poly.area = 100  # Should not be assignable

    poly.color = "#00FF00"
    assert poly.color == "#00FF00"  # RGB Conversion


def test_colored_unary_union_separate():
    poly1 = ColorPolygon("ff5733", [(0, 0), (2, 0), (1, 1)])
    poly2 = ColorPolygon("33ff57", [(3, 3), (5, 3), (4, 4)])

    result = colored_unary_union([poly1, poly2])

    assert isinstance(result, ColorMultiPolygon)
    assert len(result) == 2
    assert result[0].color == poly1.color
    assert result[1].color == poly2.color


# 7️⃣ Unary Union Should Merge Overlapping Polygons
def test_colored_unary_union_merge():
    poly1 = ColorPolygon("#FF5733", [(0, 0), (1, 0), (1, 1), (0, 1)])
    poly2 = ColorPolygon("#FF5733", [(1, 0), (2, 0), (2, 1), (1, 1)])  # Overlapping

    result = colored_unary_union([poly1, poly2])
    assert isinstance(result, ColorMultiPolygon)  # Should be merged
    assert len(result.geoms) == 1  # Contains single polygon - Indicates a merge
    assert result.geoms[0].color == poly1.color  # Uses first polygon's color
