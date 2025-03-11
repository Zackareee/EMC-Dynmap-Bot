from shapely.geometry import Polygon, MultiPolygon
from PIL import ImageColor


class ColorMultiPolygon:
    def __init__(self, *args, **kwargs):
        # Initialize the internal MultiPolygon with given arguments (e.g., a list of Polygons)
        self._multipolygon = MultiPolygon(*args, **kwargs)
        self.color = None  # default color is None

    def __getattr__(self, name):
        # Delegate attribute access to the internal MultiPolygon object
        return getattr(self._multipolygon, name)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

class ColorPolygon:
    def __init__(self, *args, **kwargs):
        # Create an internal Polygon instance
        self._polygon = Polygon(*args, **kwargs)
        self.color = None  # Default to None

    def __getattr__(self, name):
        # Delegate attribute access to the underlying Polygon object
        return getattr(self._polygon, name)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)