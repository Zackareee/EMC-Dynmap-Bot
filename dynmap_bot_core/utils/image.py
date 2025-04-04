__all__ = [
    "stitch_images",
    "draw_polygons_on_image",
    "draw_polygons_on_image",
    "crop_image",
    "resize_image",
]

from PIL import Image, ImageDraw
from dynmap_bot_core.models.spatial.chunk import Chunk
from dynmap_bot_core.models.spatial.map import Map
from dynmap_bot_core.models.spatial.coordinate import Coordinate
from shapely.geometry import Polygon


def stitch_images(images: dict[Coordinate, Image]) -> Image:
    """
    Collates all images in a dictionary into a single image, placing them at their corresponding coordinate.
    :param images: A dictionary of image coordinates to image.
    :return: A single Image object.
    """
    # Directory containing images
    TILESIZE: int = 512
    x_coords: list[int] = [coord.x for coord in images.keys()]
    z_coords: list[int] = [coord.z for coord in images.keys()]

    min_x, max_x = min(x_coords), max(x_coords)
    min_z, max_z = min(z_coords), max(z_coords)

    # Calculate canvas size
    canvas_width: int = (max_x - min_x + 1) * TILESIZE
    canvas_height: int = (max_z - min_z + 1) * TILESIZE

    # Create a blank canvas with a white background
    canvas: Image = Image.new(mode="RGBA", size=(canvas_width, canvas_height), color="white")

    # Place images on the canvas
    for coord, img in images.items():
        paste_x: int = (coord.x - min_x) * TILESIZE
        paste_y: int = (coord.z - min_z) * TILESIZE  # Corrected Y-axis logic
        canvas.paste(img, (paste_x, paste_y))
    return canvas


def draw_polygons_on_image(polygons: [Polygon], canvas: Image) -> Image:
    """
    Draws a filled polygon on the canvas with transparency.
    :param canvas: The canvas Image object.
    :param polygons: List of ColorPolygons to draw onto the image.
    """

    overlay = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    for polygon in polygons:
        draw.polygon(polygon.points(), fill=polygon.color, outline="black")

    return Image.alpha_composite(canvas, overlay)


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
    """
    offset: list[int] = mcmap.get_region_offset()
    mcmap.normalise()
    mcmap.offset_towns(-Chunk.SIZE, 0, -Chunk.SIZE)
    mcmap.offset_towns(offset[0], 0, offset[1])
    return crop_image(
        image=imgobj,
        top_left=mcmap.get_polygon_top_left_corner(),
        bottom_right=mcmap.get_polygon_bottom_right_corner(),
    )


def crop_image(image: Image, top_left: Coordinate, bottom_right: Coordinate) -> Image:
    """
    Crop an image given the top left coordinate and bottom right coordinate.
    Adds a pading of 2x the chunk size (Statically set to 16 here)
    """
    crop = (
        top_left.x,
        top_left.z,
        bottom_right.x + (16 * 2),
        bottom_right.z + (16 * 2),
    )
    return image.crop(crop)
