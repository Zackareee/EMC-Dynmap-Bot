__all__ = ["sanitize_filename"]
import urllib.parse


def unpack_town_coordinates(town_json: dict) -> list[list[int, int]]:
    """
    Given a dictionary of a town object, return all coordinates
    :param town_json: Town object as a dictionary.
    :return: list of ints for all coordinates.
    """
    coordinates: list[list[int, int]] = [town_json["coordinates"]["townBlocks"]]
    return coordinates


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
