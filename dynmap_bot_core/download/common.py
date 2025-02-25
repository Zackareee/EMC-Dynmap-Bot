__all__ = ["download_town", "download_nation"]
import requests
import json
import urllib.parse


def download_town(name: str) -> dict:
    """
    Downloads a json object from the town api endpoint.
    This JSON will be in a format found at https://earthmc.net/docs/api#towns
    :param name: A string of a town to get the json for.
    :return: A json blob of the towns details.
    """
    url: str = "https://api.earthmc.net/v3/aurora/towns"
    x: requests.Response = requests.post(url, json={"query": [name]})
    town: dict = json.loads(x.text)[0]
    return town


def download_nation(name: str) -> dict:
    """
    Downloads a json object from the nation api endpoint.
    This JSON will be in a format found at https://earthmc.net/docs/api#nations
    :param name: A string of a nation to get the json for.
    :return: A json blob of the nations details.
    """
    url: str = "https://api.earthmc.net/v3/aurora/nations"
    x: requests.Response = requests.post(url, json={"query": [name]})
    nation: dict = json.loads(x.text)[0]
    return nation

def sanitize_filename(filename: str) -> str:
    """
    Serves as a helper function for tests to sanitize a filename to meet the windows filename requirements.
    Use urllib.parse.unquote(str) to recover the filename.
    :param filename:
    :return:
    """
    safe_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.() "
    sanitized = urllib.parse.quote(filename, safe=safe_chars)
    sanitized = sanitized.rstrip(" .")
    return sanitized
