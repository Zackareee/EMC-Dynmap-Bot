from dynmap_bot_core.engine import coordinate
from dynmap_bot_core.images import image
from PIL import Image

# TODO mock these with static towns and/or json data.
# This currently just acts an an entry point to manually test.
def test_coordinates_with_map():
    town_names: list[str] = ["Sanctuary","Gulf_Of_Guinea"]
    map_obj: coordinate.Map = coordinate.build_map(town_names)

    normalised_map: coordinate.Map = map_obj.get_normalised_map()
    offset: list[int] = map_obj.get_region_offset()
    offset_map: coordinate.Map = normalised_map.offset_towns(offset[0], 0, offset[1])

    image_obj: Image = coordinate.build_image_with_map(map_obj)
    cropped_image: Image = image.crop_image(
        image=image_obj,
        top_left=offset_map.get_polygon_top_left_corner(),
        bottom_right=offset_map.get_polygon_bottom_right_corner(),
    )
    image.resize_image(cropped_image).show()
