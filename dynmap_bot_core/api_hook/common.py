__all__ = ["get_town"]
from dynmap_bot_core import download
import requests
import json
from dynmap_bot_core.orm import orm

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


def get_players(uuid: str) -> dict:
    url: str = "https://api.earthmc.net/v3/aurora/players"
    x: requests.Response = requests.post(url, json={"query": [uuid]})
    player: dict = json.loads(x.text)[0]
    return player

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
