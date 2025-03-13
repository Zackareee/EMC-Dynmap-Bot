__all__ = ["map_images_as_dict"]
from dynmap_bot_core.models.spatial.coordinate import Coordinate
from PIL import Image
from io import BytesIO
import requests
import json


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


def map_images_as_dict(regions: list[Coordinate]) -> dict[Coordinate, Image]:
    """
    Given a list of region objects (x, z) these will be returned in a dictionary with an image object associated with
    each coordinate.
    :param regions: A list of (x, z) values where x and z are integers.
    :return: A dictionary of coordinates to image objects.
    """
    region_images = {}
    for coord in regions:
        if coord not in region_images.keys():
            region_images[coord] = download_map_image(coord)
    return region_images


def download_map_image(coord: Coordinate) -> Image:
    """
    Given x and z coordinates, the tile png will be returned as an Image object
    TODO consider taking a Coordinate object
    :param x: Int
    :param z: Int
    :return: Image object
    """
    with requests.get(f"https://map.earthmc.net/tiles/minecraft_overworld/3/{coord.x}_{coord.z}.png") as r:
        r.raise_for_status()
        return Image.open(BytesIO(r.content))
