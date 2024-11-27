__all__ = ["download", "download_map_image"]

import requests
import os
from PIL import Image, ImageDraw
from io import BytesIO

s: str = "#" if os.name == "nt" else "-"

# def download_map_image(x: int, z: int) -> None:
#     download(f"https://map.earthmc.net/tiles/minecraft_overworld/3/{x}_{z}.png",
#              rf"C:\Users\zacka\Documents\Projects\EMC-Dynmap-Bot\out\images\{x}_{z}.png")


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

    #
    #
    #
    # headers: dict[str, str] = _get_headers()
    #
    # request_body: requests.Response = requests.get(
    #     url=url,
    #     headers=headers,
    # )
    #
    # if b"502: Bad gateway" in request_body.content:
    #     print("502: Bad gateway")
    #     return False
    #
    # open(file=filepath, mode="w").write(request_body.content)
    # return True


def download_json(url, filepath: str) -> bool:
    headers: dict[str, str] = _get_headers()

    request_body: requests.Response = requests.get(
        url=url,
        headers=headers,
    )

    if b"502: Bad gateway" in request_body.content:
        print("502: Bad gateway")
        return False

    open(file=filepath, mode="wb").write(request_body.content)
    return True


# pickle_063 = get_players("9cd95f3e-d22e-4010-9beb-aaa642da38c3")
# player = orm.Player(
#     uuid=pickle_063["uuid"],
#     name=pickle_063["name"],
#     town_id=pickle_063["town"]["uuid"],
# )
# from dynmap_bot_core.models import town as t
# import sqlalchemy as sa
# town = get_town(player.town_id)
# town = orm.Town(
#     uuid = town["uuid"],
#     name = town["name"],
#     coordinates = str(town["coordinates"]),
# )
# town = town
#
# dbEngine = sa.create_engine(r'sqlite:////Users\zacka\Documents\Projects\EMC-Dynmap-Bot\dynmap_bot_core\orm\database.db') # ensure this is the correct path for the sqlite file.
# session = sa.orm.Session(dbEngine)
#
# session.merge(town)  # Automatically updates if a row with the same primary key exists
# session.merge(player)
# session.commit()
#
#
#
#
#
# # for town in result:
# #     town = town
# #
# # val = pd.read_sql('select * from Town',dbEngine)
# # pass
#
#
# pass
# pass
