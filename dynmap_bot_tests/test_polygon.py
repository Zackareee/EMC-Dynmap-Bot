import pytest
from shapely.geometry import Polygon
from dynmap_bot_core.engine.colorpolygon import ColorPolygon, ColorMultiPolygon, colored_unary_union


def test_coloredpolygon_instantiation():
    poly = ColorPolygon([(0, 0), (1, 1), (1, 0)])
    assert isinstance(poly, ColorPolygon)
    assert isinstance(poly._polygon, Polygon)
    assert poly.area == Polygon([(0, 0), (1, 1), (1, 0)]).area


def test_coloredpolygon_coordinates():
    poly = ColorPolygon([(0, 0), (1, 1), (1, 0)])
    assert list(poly.exterior.coords) == list(Polygon([(0, 0), (1, 1), (1, 0)]).exterior.coords)

def test_coloredpolygon_polygon_methods():
    poly = ColorPolygon([(0, 0), (1, 1), (1, 0)])
    assert poly.area == Polygon([(0, 0), (1, 1), (1, 0)]).area
    assert poly.bounds == Polygon([(0, 0), (1, 1), (1, 0)]).bounds


def test_coloredpolygon_immutable():
    poly = ColorPolygon([(0, 0), (1, 1), (1, 0)])

    with pytest.raises(AttributeError):
        poly.area = 100  # Should not be assignable

    poly.color = "00ff00"
    assert poly.color == "00ff00"  # RGB Conversion


def test_colored_unary_union_separate():
    poly1 = ColorPolygon([(0, 0), (2, 0), (1, 1)])
    poly2 = ColorPolygon([(3, 3), (5, 3), (4, 4)])

    poly1.color = "ff5733"
    poly2.color = "33ff57"

    result = colored_unary_union([poly1, poly2])

    assert isinstance(result, ColorMultiPolygon)
    assert len(result) == 2
    assert result[0].color == poly1.color
    assert result[1].color == poly2.color


# 7️⃣ Unary Union Should Merge Overlapping Polygons
def test_colored_unary_union_merge():
    poly1 = ColorPolygon([(0, 0), (1, 0), (1, 1), (0, 1)])
    poly2 = ColorPolygon([(1, 0), (2, 0), (2, 1), (1, 1)])  # Overlapping

    poly1.color = "ff5733"
    poly2.color = "33ff57"

    result = colored_unary_union([poly1, poly2])
    assert isinstance(result, ColorPolygon)  # Should be merged
    assert result.color == poly1.color # Uses first polygon's color
