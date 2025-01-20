__all__ = ["download", "download_map_image", "download_map_images_as_dict"]

import requests
import os
from PIL import Image, ImageDraw
from io import BytesIO
import math
from dynmap_bot_core.engine.overlap import coordinate
s: str = "#" if os.name == "nt" else "-"

# def download_map_image(x: int, z: int) -> None:
#     download(f"https://map.earthmc.net/tiles/minecraft_overworld/3/{x}_{z}.png",
#              rf"C:\Users\zacka\Documents\Projects\EMC-Dynmap-Bot\out\images\{x}_{z}.png")

def download_map_images_as_dict(blocks: list[coordinate.Coordinate]):
    images = {}
    for coord in blocks:
        if (coord.x, coord.z) not in images.keys():
            images[(coord.x, coord.z)] = download_map_image(int(coord.x), int(coord.z))
    return images

def download_map_image(x: int, z: int) -> bytes:
    with requests.get(
        f"https://map.earthmc.net/tiles/minecraft_overworld/3/{x}_{z}.png"
    ) as r:
        r.raise_for_status()
        # with open(filepath, 'wb') as f:
        #     for chunk in r.iter_content(chunk_size=8192):
        #         f.write(chunk)
        return Image.open(BytesIO(r.content))


def _get_headers() -> dict[str, str]:
    headers: dict[str, str] = {
        "User-Agent": """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"""
    }
    return headers


def download(url, filepath: str) -> bool:

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return True
