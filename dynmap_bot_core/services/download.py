__all__ = ["map_images_as_dict"]


from dynmap_bot_core.models.spatial.coordinate import Coordinate
from PIL import Image
from io import BytesIO
import requests
import json
import asyncio
from dynmap_bot_core.services.parallel_download import download_region_images


def download_towns(name: [str]) -> dict:
    """
    Downloads a json object from the town api endpoint.
    This JSON will be in a format found at https://earthmc.net/docs/api#towns
    :param name: A string of a town to get the json for.
    :return: A json blob of the towns details.
    """
    url: str = "https://api.earthmc.net/v3/aurora/towns"
    x: requests.Response = requests.post(url, json={"query": name})
    towns: dict = json.loads(x.text)
    return towns


def download_nations(name: [str]) -> dict:
    """
    Downloads a json object from the nation api endpoint.
    This JSON will be in a format found at https://earthmc.net/docs/api#nations
    :param name: A string of a nation to get the json for.
    :return: A json blob of the nations details.
    """
    url: str = "https://api.earthmc.net/v3/aurora/nations"
    x: requests.Response = requests.post(url, json={"query": name})
    nation: dict = json.loads(x.text)
    return nation


def generate_rectangle_coordinates(coords: list[Coordinate]) -> list[Coordinate]:
    if not coords:
        return []

    # Find min and max values for x and z
    min_x = min(coord.x for coord in coords)
    max_x = max(coord.x for coord in coords)
    min_z = min(coord.z for coord in coords)
    max_z = max(coord.z for coord in coords)

    # Generate all points within the rectangle
    rectangle_coords = [Coordinate(x, 0, z) for x in range(min_x, max_x + 1) for z in range(min_z, max_z + 1)]

    return rectangle_coords


def map_images_as_dict(regions: list[Coordinate]) -> dict[Coordinate, Image]:
    """
    Given a list of region objects (x, z) these will be returned in a dictionary with an image object associated with
    each coordinate.
    :param regions: A list of (x, z) values where x and z are integers.
    :return: A dictionary of coordinates to image objects.
    """
    regions = generate_rectangle_coordinates(regions)
    return asyncio.run(download_region_images(regions))
