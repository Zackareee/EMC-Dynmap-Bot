__all__ = ["map_images_as_dict"]

import requests
from PIL import Image
from io import BytesIO

def map_images_as_dict(regions: list["Coordinate"]) -> dict[tuple[int,int], Image]:
    """
    Given a list of region objects (x, z) these will be returned in a dictionary with an image object associated with
    each coordinate.
    TODO consider returning dict[tuple[Coordinate],Image]
    :param regions: A list of (x, z) values where x and z are integers.
    :return: A dictionary of coordinates to image objects.
    """
    region_images = {}
    for coord in regions:
        if (coord.x, coord.z) not in region_images.keys():
            x = int(coord.x)
            z = int(coord.z)
            region_images[(x,z)] = download_map_image(x, z)
    return region_images


def download_map_image(x: int, z: int) -> Image:
    """
    Given x and z coordinates, the tile png will be returned as an Image object
    TODO consider taking a Coordinate object
    :param x: Int
    :param z: Int
    :return: Image object
    """
    with requests.get(
        f"https://map.earthmc.net/tiles/minecraft_overworld/3/{x}_{z}.png"
    ) as r:
        r.raise_for_status()
        return Image.open(BytesIO(r.content))