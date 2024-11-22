__all__ = ["download_json"]

import requests
import os
from datetime import datetime

import pathlib

s: str = "#" if os.name == "nt" else "-"


def _get_headers() -> dict[str, str]:
    headers: dict[str, str] = {
        "User-Agent": """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"""
    }
    return headers


def _get_emc_towny_url() -> str:
    return "https://map.earthmc.net/tiles/minecraft_overworld/markers.json"


def download_json(url, filepath: str) -> bool:
    """

    :param server_name:
    :return:
    """
    headers: dict[str, str] = _get_headers()

    json_body: requests.Response = requests.get(
        url=url,
        headers=headers,
    )

    if b"502: Bad gateway" in json_body.content:
        print("502: Bad gateway")
        return False

    open(file=filepath, mode="wb").write(json_body.content)
    return True
