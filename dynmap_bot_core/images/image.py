import PIL
import random
from shapely.geometry import Polygon
from shapely.ops import unary_union


def make_image_collage(images) -> PIL.Image:
    # Directory containing images
    TILESIZE = 512
    x_coords = [coord[0] for coord in images.keys()]
    z_coords = [coord[1] for coord in images.keys()]

    min_x, max_x = min(x_coords), max(x_coords)
    min_z, max_z = min(z_coords), max(z_coords)

    # Calculate canvas size
    canvas_width = (max_x - min_x + 1) * TILESIZE
    canvas_height = (max_z - min_z + 1) * TILESIZE

    # Create a blank canvas with a white background
    canvas = PIL.Image.new(
        mode="RGBA", size=(canvas_width, canvas_height), color="white"
    )

    # Place images on the canvas

    for (x, y), img in images.items():
        paste_x = (x - min_x) * TILESIZE
        paste_y = (y - min_z) * TILESIZE  # Corrected Y-axis logic
        canvas.paste(img, (paste_x, paste_y))
    return canvas


def make_grids_on_collage(polygon, canvas) -> PIL.Image:

    polygon_coords = [[int(x), int(z)] for x, z in polygon.exterior.coords]

    color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        int(255 * 0.5),
    )

    res = list(tuple(a + 8 for a in sub) for sub in polygon_coords)

    canvas = draw_filled_polygon(canvas, res, color)

    return canvas


def draw_filled_polygon(canvas, points, color):
    """
    Draws a filled polygon on the canvas with transparency.
    :param canvas: The canvas Image object.
    :param points: List of (x, y) coordinates for the polygon.
    :param color: List of (R, G, B, A) values.

    """
    # Create a transparent overlay
    overlay = PIL.Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    draw = PIL.ImageDraw.Draw(overlay)
    draw.polygon(points, fill=color, outline="black")

    # Composite the overlay onto the original canvas
    return PIL.Image.alpha_composite(canvas.convert("RGBA"), overlay)
