from dynmap_bot_core.api_hook import common
from dynmap_bot_core.engine.overlap import coordinate
from dynmap_bot_core.orm import orm
from dynmap_bot_core import download as dl
import os
from PIL import Image, ImageDraw

#
#

#     pass

def test_images():
    vladivostok = orm.unpack_town_response(common.get_town("aomi"))
    # khogno_khan = orm.unpack_town_response(common.get_town("Khogno_Khan"))
    coordinates = coordinate.get_coordinates(vladivostok)
    image_coordinates = coordinate.get_image_coordinates(coordinates)
    for i in image_coordinates:
        dl.download_map_image(i[0], i[1])
    min_x, min_z = coordinate.get_min_coordinates_2d(image_coordinates)
    min_x *= 32
    min_z *= 32
    offset_coordinates = coordinate.normalise_coordinates(coordinates, min_x, min_z)
    make_image_collage(offset_coordinates)


def make_image_collage(polygon_coords):
    # Directory containing images
    image_dir = r"C:\Users\zacka\Documents\Projects\EMC-Dynmap-Bot\out\images"
    output_file = r"C:\Users\zacka\Documents\Projects\EMC-Dynmap-Bot\output_collage_with_polygon.png"

    # Image dimensions (512x512 px)
    tile_size = 512

    images = {}
    for filename in os.listdir(image_dir):
        if filename.endswith(".png"):
            coords = parse_coordinates(filename)
            if coords:
                images[coords] = os.path.join(image_dir, filename)

    # Determine canvas bounds
    if not images:
        print("No valid images found.")
        exit()

    x_coords = [coord[0] for coord in images.keys()]
    y_coords = [coord[1] for coord in images.keys()]
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    # Calculate canvas size
    canvas_width = (max_x - min_x + 1) * tile_size
    canvas_height = (max_y - min_y + 1) * tile_size

    # Create a blank canvas with a white background
    canvas = Image.new("RGBA", (canvas_width, canvas_height), "white")

    # Place images on the canvas
    for (x, y), filepath in images.items():
        img = Image.open(filepath)
        paste_x = (x - min_x) * tile_size
        paste_y = (y - min_y) * tile_size  # Corrected Y-axis logic
        canvas.paste(img, (paste_x, paste_y))

    # Draw a filled polygon
    for i in polygon_coords:
        i = sorted(i)
        # i = coordinate.calculate_perimeter(i)
        res = list(tuple(a*16 for a in sub) for sub in i)

        draw_filled_polygon(canvas, res)

    # canvas.show()
    # Save the final collage
    canvas.save(output_file)




def parse_coordinates(filename):
    """Extract coordinates from the filename."""
    base_name = os.path.splitext(filename)[0]
    try:
        x, y = map(int, base_name.split('_'))
        return x, y
    except ValueError:
        return None


def draw_filled_polygon(canvas, points):
    """
    Draws a filled polygon on the canvas with transparency.
    :param canvas: The canvas Image object.
    :param points: List of (x, y) coordinates for the polygon.
    """
    # Create a transparent overlay
    overlay = Image.new("RGBA", canvas.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    # Draw the semi-transparent rectangles on the overlay
    for i in points:
        shape = [(i[0], i[1]), (i[0] + 16, i[1] + 16)]
        draw.rectangle(shape, fill=(255, 0, 0, int(255 * 0.4)))  # 20% transparency

    # Composite the overlay onto the original canvas
    result = Image.alpha_composite(canvas.convert("RGBA"), overlay)

    # Display the result
    result.show()
    # print(f"Collage saved to {output_file}")

# Collect all images with valid coordinates


