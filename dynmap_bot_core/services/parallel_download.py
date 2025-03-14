import aiohttp
import asyncio
from io import BytesIO
from PIL import Image
from tqdm.asyncio import tqdm
from typing import Dict, List
from dynmap_bot_core.models.spatial.coordinate import Coordinate

MAX_CONNECTIONS = 500


async def download_image(session, url, semaphore):
    """Asynchronously downloads an image and returns it as a PIL Image."""
    async with semaphore:
        for attempt in range(3):
            try:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        img_data = await response.read()
                        return Image.open(BytesIO(img_data))
            except Exception as e:
                if attempt == 2:
                    print(f"Failed: {url} | Error: {e}")
    return None


async def download_region_images(coordinate_lists: List[Coordinate]) -> Dict[Coordinate, Image]:
    """Downloads images based on provided lists of Coordinate objects and returns a dictionary mapping coordinates to PIL images."""
    urls = {
        coord: f"https://map.earthmc.net/tiles/minecraft_overworld/3/{coord.x}_{coord.z}.png"
        for coord in coordinate_lists
    }

    print(f"Total URLs: {len(urls)}")

    connector = aiohttp.TCPConnector(limit=0)
    headers = {"Accept-Encoding": "gzip"}

    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        semaphore = asyncio.Semaphore(MAX_CONNECTIONS)
        tasks = {coord: download_image(session, url, semaphore) for coord, url in urls.items()}

        results = await tqdm.gather(*tasks.values(), total=len(urls))
        return {coord: img for coord, img in zip(tasks.keys(), results) if img is not None}


def map_images_as_dict(regions: List[Coordinate]) -> Dict[Coordinate, Image]:
    """
    Given a list of region objects (x, z), these will be returned in a dictionary with an image object associated with
    each coordinate.
    :param regions: A list of Coordinate objects.
    :return: A dictionary mapping Coordinates to PIL Image objects.
    """
    return download_images(regions)
