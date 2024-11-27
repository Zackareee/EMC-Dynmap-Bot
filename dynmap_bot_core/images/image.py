import PIL
import random
from dynmap_bot_core.engine.overlap import coordinate
def get_chunk_size() -> int:
    return 1

# def a_crude_ass_way_of_collating_perimeters(grid_points: list[list[list[int, int]]]):
#     left = set()
#     top = set()
#     right = set()
#     bottom = set()
#
#     for pair in grid_points:
#         line_dict = make_square_lines(pair)
#         left.add(line_dict["left"])
#         right.add(line_dict["right"])
#         top.add(line_dict["top"])
#         bottom.add(line_dict["bottom"])
#
#     #find duplicates
#     duplicates_lr: set = left.intersection(right)
#     duplicates_tb: set = top.intersection(bottom)
#
#     unique_lr = (left.union(right)).difference(duplicates_lr)
#     unique_tb = (top.union(bottom)).difference(duplicates_tb)
#
#     perimeter_points = unique_lr.union(unique_tb)
#     coordinates = set()
#     for point_pair in perimeter_points:
#         for coordinate in point_pair:
#             coordinates.add(coordinate)
#     return list(coordinates)
#
#
# def make_square_lines(point: list[int,int]) -> dict[str,list[list[int, int]]]:
#     CHUNKSIZE = get_chunk_size()
#     x = point[0]
#     z = point[1]
#     left = ((x, z), (x+CHUNKSIZE, z))
#     top = ((x, z), (x, z+CHUNKSIZE))
#     bottom = ((x+CHUNKSIZE, z), (x+CHUNKSIZE, z+CHUNKSIZE))
#     right =((x, z+CHUNKSIZE), (x+CHUNKSIZE, z+CHUNKSIZE))
#     return {
#         "left": left,
#         "right": right,
#         "top": top,
#         "bottom": bottom
#     }

def custom_intersection(set_A, set_B):
    # Create a new set for the intersection, only considering exact matches
    return set(tuple(sorted(pair)) for pair in set_A).intersection(set(tuple(sorted(pair)) for pair in set_B))

def custom_intersection_v2(set_A, set_B):
    # Create a new set for the intersection, only considering exact matches
    return set(tuple(sorted(pair)) for pair in set_A).intersection(set(tuple(pair) for pair in set_B))

def tuple_set_intersection(set_A, set_B):
    # Create a new set for the intersection of the two sets
    intersection = set()

    # Loop through each tuple in set_A
    for tup_a in set_A:
        # For each tuple in set_A, check if its reversed tuple exists in set_B
        if tup_a[::-1] in set_B:
            # If found, add the tuple itself (not reversed) to the intersection
            intersection.add(tup_a)

    return intersection


def a_crude_ass_way_of_collating_perimeters(grid_points: list[list[list[int, int]]]):
    left = set()
    top = set()
    right = set()
    bottom = set()

    for pair in grid_points:
        line_dict = make_square_lines(pair)
        left.add(line_dict["left"])
        right.add(line_dict["right"])
        top.add(line_dict["top"])
        bottom.add(line_dict["bottom"])

    #find duplicates
    duplicates_left: set = tuple_set_intersection(left, right)
    duplicates_right: set = tuple_set_intersection(right, left)
    duplicates_top: set = tuple_set_intersection(top, bottom)
    duplicates_bottom: set = tuple_set_intersection(bottom, top)

    new_left = left.difference(duplicates_left)
    new_right = right.difference(duplicates_right)
    new_top = top.difference(duplicates_top)
    new_bottom = bottom.difference(duplicates_bottom)

    cyclic_list = make_linked_list_of_coordinates(new_left,new_right,new_top,new_bottom)
    return cyclic_list

def make_linked_list_of_coordinates(left,right,top,bottom):
    # Start with an arbitrary origin (e.g., from 'left' set)
    all_sets = {'left': left, 'right': right, 'top': top, 'bottom': bottom}
    origin = next(iter(left))[0]  # Start with the first origin from the 'left' set

    # Create the linked list of coordinates
    linked_list = [origin]  # Initialize the linked list with the first origin

    # We will keep track of visited origins to avoid revisiting
    visited_origins = {origin}

    while len(visited_origins) < len(left) + len(right) + len(top) + len(bottom):
        found_next = False
        # Search for the destination in each set
        for direction, coordinates in all_sets.items():
            if not found_next:
                for origin_point, destination_point in coordinates:
                    if origin_point == origin and destination_point not in visited_origins:
                        # Add the destination as the next origin
                        linked_list.append(destination_point)
                        visited_origins.add(destination_point)
                        origin = destination_point  # Set new origin
                        found_next = True
                        break

    return linked_list

def make_square_lines(point: list[int,int]) -> dict[str,list[list[int, int]]]:
    CHUNKSIZE = get_chunk_size()
    x = point[0]
    z = point[1]
    top = ((x, z), (x, z+CHUNKSIZE))
    right =((x, z+CHUNKSIZE), (x+CHUNKSIZE, z+CHUNKSIZE))
    bottom = ((x+CHUNKSIZE, z+CHUNKSIZE), (x+CHUNKSIZE, z))
    left = ((x+CHUNKSIZE, z),(x, z))

    return {
        "left": left,
        "right": right,
        "top": top,
        "bottom": bottom
    }

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
    canvas = PIL.Image.new(mode="RGBA", size=(canvas_width, canvas_height), color="white")

    # Place images on the canvas

    for (x, y), img in images.items():
        paste_x = (x - min_x) * TILESIZE
        paste_y = (y - min_z) * TILESIZE  # Corrected Y-axis logic
        canvas.paste(img, (paste_x, paste_y))
    return canvas

def make_grids_on_collage(polygon_coords, canvas) -> PIL.Image:
    for i in polygon_coords:
        color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
            int(255 * 0.5),
        )
        res = list(
            tuple(
                a * 16 for a in sub
            ) for sub in i
        )
        # res = coordinate.reorder_cyclic_list(res)

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


# def make_image_collage(polygon_coords, images) -> PIL.Image:
#     # Directory containing images
#     TILESIZE = 512
#     x_coords = [coord[0] for coord in images.keys()]
#     z_coords = [coord[1] for coord in images.keys()]
#
#     min_x, max_x = min(x_coords), max(x_coords)
#     min_z, max_z = min(z_coords), max(z_coords)
#
#     # Calculate canvas size
#     canvas_width = (max_x - min_x + 1) * TILESIZE
#     canvas_height = (max_z - min_z + 1) * TILESIZE
#
#     # Create a blank canvas with a white background
#     canvas = PIL.Image.new(mode="RGBA", size=(canvas_width, canvas_height), color="white")
#
#     # Place images on the canvas
#     for (x, y), img in images.items():
#         paste_x = (x - min_x) * TILESIZE
#         paste_y = (y - min_z) * TILESIZE  # Corrected Y-axis logic
#         canvas.paste(img, (paste_x, paste_y))
#
#     # Draw a filled polygon
#     for i in polygon_coords:
#         color = (
#             random.randint(0, 255),
#             random.randint(0, 255),
#             random.randint(0, 255),
#             int(255 * 0.5),
#         )
#         res = list(
#             tuple(
#                 a * 16 for a in sub
#             ) for sub in sorted(i)
#         )
#
#         canvas = draw_filled_polygon(canvas, res, color)
#
#     return canvas



# def draw_filled_polygon(canvas, points, color):
#     """
#     Draws a filled polygon on the canvas with transparency.
#     :param canvas: The canvas Image object.
#     :param points: List of (x, y) coordinates for the polygon.
#     :param color: List of (R, G, B, A) values.
#
#     """
#     # Create a transparent overlay
#     overlay = PIL.Image.new("RGBA", canvas.size, (255, 255, 255, 0))
#     draw = PIL.ImageDraw.Draw(overlay)
#     # Draw the semi-transparent rectangles on the overlay
#     for i in points:
#         shape = [(i[0], i[1]), (i[0] + 16, i[1] + 16)]
#         draw.rectangle(shape, fill=color, outline="black")
#
#     # Composite the overlay onto the original canvas
#     return PIL.Image.alpha_composite(canvas.convert("RGBA"), overlay)
