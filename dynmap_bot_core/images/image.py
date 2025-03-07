__all__ = [
    "make_image_collage",
    "make_grids_on_collage",
    "draw_filled_polygon",
    "crop_image",
    "resize_image",
]

from PIL import Image, ImageDraw
import random
from dynmap_bot_core.engine.map import Map
from dynmap_bot_core.engine.coordinate import Coordinate
from shapely.geometry import Polygon


def make_image_collage(images: dict[tuple[int, int], Image]) -> Image:
    """
    Collates all images in a dictionary into a single image, placing them at their corresponding coordinate.
    :param images: A dictionary of image coordinates to image.
    :return: A single Image object.
    """
    # Directory containing images
    TILESIZE: int = 512
    x_coords: list[int] = [coord[0] for coord in images.keys()]
    z_coords: list[int] = [coord[1] for coord in images.keys()]

    min_x, max_x = min(x_coords), max(x_coords)
    min_z, max_z = min(z_coords), max(z_coords)

    # Calculate canvas size
    canvas_width: int = (max_x - min_x + 1) * TILESIZE
    canvas_height: int = (max_z - min_z + 1) * TILESIZE

    # Create a blank canvas with a white background
    canvas: Image = Image.new(
        mode="RGBA", size=(canvas_width, canvas_height), color="white"
    )

    # Place images on the canvas
    for (x, y), img in images.items():
        paste_x: int = (x - min_x) * TILESIZE
        paste_y: int = (y - min_z) * TILESIZE  # Corrected Y-axis logic
        canvas.paste(img, (paste_x, paste_y))
    return canvas


def create_random_colour() -> tuple[int, int, int, int]:
    """
    Creates a tuple representing an RGBA value
    :return: tuple
    """
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        int(255 * 0.5),
    )


def make_grids_on_collage(polygon: Polygon, canvas: Image) -> Image:
    """
    Draws polygons onto an Image object, returning the modified Image.
    TODO consider refactoring this method, the types are unpleasant. ALSO rename this method
    :param polygon:
    :param canvas:
    :return:
    """
    polygon_coords: list[list[int]] = [
        [int(x), int(z)] for x, z in polygon.exterior.coords
    ]
    color: tuple[int, int, int, int] = create_random_colour()
    res: list[tuple[int, ...]] = list(
        tuple(a + 8 for a in sub) for sub in polygon_coords
    )
    canvas: Image = draw_filled_polygon(canvas, res, color)

    return canvas


def draw_filled_polygon(canvas: Image, points, color: tuple[int, int, int, int]):
    """
    Draws a filled polygon on the canvas with transparency.
    :param canvas: The canvas Image object.
    :param points: List of (x, y) coordinates for the polygon.
    :param color: List of (R, G, B, A) values.

    """
    # Create a transparent overlay
    overlay = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    draw.polygon(points, fill=color, outline="black")

    # Composite the overlay onto the original canvas
    return Image.alpha_composite(canvas.convert("RGBA"), overlay)


def resize_image(image: Image) -> Image:
    """
    Scale an image 4x
    :param image:
    :return:
    """
    width, height = image.size
    return image.resize(size=(width * 4, height * 4), resample=Image.Resampling.NEAREST)


def crop_map_and_image(mcmap: Map, imgobj: Image) -> Image:
    """
    Crop an image given the top left coordinate and bottom right coordinate.
    Adds a pading of 2x the chunk size (Statically set to 16 here)
    TODO refactor this so chunk.SIZE can be imported without a circular import, and Coordinate can be used
    """
    normalised_map: Map = mcmap.get_normalised_map()
    normalised_map: Map = normalised_map.offset_towns(-16, 0, -16)

    offset: list[int] = mcmap.get_region_offset()
    offset_map: Map = normalised_map.offset_towns(offset[0], 0, offset[1])
    return crop_image(
        image=imgobj,
        top_left=offset_map.get_polygon_top_left_corner(),
        bottom_right=offset_map.get_polygon_bottom_right_corner(),
    )


def crop_image(image: Image, top_left: Coordinate, bottom_right: Coordinate) -> Image:
    """
    Crop an image given the top left coordinate and bottom right coordinate.
    Adds a pading of 2x the chunk size (Statically set to 16 here)
    TODO refactor this so chunk.SIZE can be imported without a circular import, and Coordinate can be used
    """
    crop = (
        top_left.x,
        top_left.z,
        bottom_right.x + (16 * 2),
        bottom_right.z + (16 * 2),
    )
    return image.crop(crop)
