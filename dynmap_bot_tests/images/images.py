from dynmap_bot_core.api_hook import common
from dynmap_bot_core.engine.overlap import coordinate
from dynmap_bot_core.orm import orm
from dynmap_bot_core import download as dl
from dynmap_bot_core.images import image as img
import PIL

def test_images():
    town_names = ["Sanctuary", "ILoveFix", "Gulf_Of_Guinea", "PearlyGates"]
    towns = [orm.unpack_town_response(common.get_town(town)) for town in town_names]

    coordinates = coordinate.get_coordinates(*towns)
    image_coordinates = coordinate.get_background_image_coordinates(coordinates)
    image_data = dl.download_map_images_as_dict(image_coordinates)

    min_x, min_z = coordinate.get_min_coordinates_2d(image_coordinates)
    min_x *= 32
    min_z *= 32
    offset_coordinates = coordinate.normalise_coordinates(coordinates, min_x, min_z)
    image: PIL.Image = img.make_image_collage(offset_coordinates, image_data)
    image.save(r"C:\Users\zacka\Documents\Projects\EMC-Dynmap-Bot\output_collage_with_polygon.png")


def test_make_square():
    img.make_square_lines([0,0])


def test_perimeter_collapsing():
    # town_names = ["Cape_Verde"]
    town_names = ["Sanctuary", "ILoveFix", "Gulf_Of_Guinea", "PearlyGates"]

    towns = [orm.unpack_town_response(common.get_town(town)) for town in town_names]
    coordinates = coordinate.get_coordinates(*towns)
    image_coordinates = coordinate.get_background_image_coordinates(coordinates)
    image_data = dl.download_map_images_as_dict(image_coordinates)
    min_x, min_z = coordinate.get_min_coordinates_2d(image_coordinates)
    offset_coordinates = coordinate.normalise_coordinates(coordinates, min_x * 32, min_z * 32)

    min_x, min_z = coordinate.get_min_coordinates_3d(offset_coordinates)
    max_x, max_z = coordinate.get_max_coordinates_3d(offset_coordinates)

    min_x *= 16
    min_x -= 16
    min_z *= 16
    min_z -= 16
    max_x *= 16
    max_x += 32
    max_z *= 16
    max_z += 32

    town_polygons = []
    for town_coordinates in offset_coordinates:
        town_polygons += [img.a_crude_ass_way_of_collating_perimeters(town_coordinates)]
    image: PIL.Image = img.make_image_collage(image_data)
    for i in town_polygons:
        image = img.make_grids_on_collage([i], image)
    image = image.crop((min_x,min_z,max_x,max_z))
    width, height = image.size
    image = image.resize((width * 4, height * 4), PIL.Image.NEAREST)
    image.show()
