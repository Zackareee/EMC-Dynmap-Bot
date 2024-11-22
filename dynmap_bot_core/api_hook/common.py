__all__ = ["get_town"]
from dynmap_bot_core import download
import requests
import json


def get_all_towns():
    url: str = "https://api.earthmc.net/v3/aurora/towns"
    x: requests.Response = requests.get(url)
    all_towns = json.loads(x.text)
    return all_towns


def get_all_nations():
    url: str = "https://api.earthmc.net/v3/aurora/nations"
    filepath: str = (
        r"C:\Users\zacka\Documents\Projects\EMC-Dynmap-Bot\in\minecraft_overworld\nations.json"
    )
    download.download_json(url=url, filepath=filepath)


def get_all_players():
    url: str = "https://api.earthmc.net/v3/aurora/players"
    filepath: str = (
        r"C:\Users\zacka\Documents\Projects\EMC-Dynmap-Bot\in\minecraft_overworld\players.json"
    )
    download.download_json(url=url, filepath=filepath)


def get_all_quaters():
    url: str = "https://api.earthmc.net/v3/aurora/quarters"
    filepath: str = (
        r"C:\Users\zacka\Documents\Projects\EMC-Dynmap-Bot\in\minecraft_overworld\quarters.json"
    )
    download.download_json(url=url, filepath=filepath)


def get_town(name: str) -> dict:
    url: str = "https://api.earthmc.net/v3/aurora/towns"
    x: requests.Response = requests.post(url, json={"query": [name]})
    town: dict = json.loads(x.text)[0]
    return town
