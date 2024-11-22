__all__ = ["unpack_town_response", "Town"]
from dataclasses import dataclass
from dynmap_bot_core.models import coordinate


@dataclass
class Player:
    name: str
    uuid: str


@dataclass
class Nation:
    name: str
    uuid: str


@dataclass
class Status:
    isPublic: bool
    isOpen: bool
    isNeutral: bool
    isCapital: bool
    isOverClaimed: bool
    isRuined: bool
    isForSale: bool
    hasNation: bool
    hasOverclaimShield: bool
    canOutsidersSpawn: bool


@dataclass
class Stats:
    numTownBlocks: int
    maxTownBlocks: int
    bonusBlocks: int
    numResidents: int
    numTrusted: int
    numOutlaws: int
    balance: float
    forSalePrice: int | None


@dataclass
class PermFlags:
    pvp: bool
    explosion: bool
    fire: bool
    mobs: bool


@dataclass
class Perms:
    build: list[bool]
    destroy: list[bool]
    switch: list[bool]
    itemUse: list[bool]
    flags: PermFlags


@dataclass
class TownCoordinates:
    spawn: dict
    homeBlock: coordinate.Coordinate
    townBlocks: list[coordinate.Coordinate]


@dataclass
class Town:
    name: str
    uuid: str
    board: str
    wiki: str
    mayor: Player
    nation: Nation
    timestamps: dict
    status: Status
    stats: Stats
    perms: Perms
    coordinates: TownCoordinates
    residents: list[Player]
    trusted: list[Player]
    outlaws: list[Player]
    quarters: list
    ranks: dict[str, str]


def unpack_town_coordinate(coordinates: dict) -> TownCoordinates:
    spawn = coordinate.Coordinate(
        x=round(coordinates["spawn"]["x"]),
        z=round(coordinates["spawn"]["z"]),
    )
    homeBlock = coordinate.Coordinate(*coordinates["homeBlock"])
    townBlocks = [coordinate.Coordinate(*i) for i in coordinates["townBlocks"]]

    return TownCoordinates(spawn=spawn, homeBlock=homeBlock, townBlocks=townBlocks)


def unpack_town_response(town_json) -> Town:
    mayor = Player(**town_json["mayor"])
    nation = Nation(**town_json["nation"])
    status = Status(**town_json["status"])
    stats = Stats(**town_json["stats"])
    flags = PermFlags(**town_json["perms"]["flags"])
    perms = Perms(
        build=town_json["perms"]["build"],
        destroy=town_json["perms"]["destroy"],
        switch=town_json["perms"]["switch"],
        itemUse=town_json["perms"]["itemUse"],
        flags=flags,
    )
    residents = [Player(**i) for i in town_json["residents"]]
    trusted = [Player(**i) for i in town_json["trusted"]]
    outlaws = [Player(**i) for i in town_json["outlaws"]]

    coordinates = unpack_town_coordinate(town_json["coordinates"])

    town_obj: Town = Town(
        name=town_json["name"],
        uuid=town_json["uuid"],
        board=town_json["board"],
        wiki=town_json["wiki"],
        mayor=mayor,
        nation=nation,
        timestamps=town_json["timestamps"],
        status=status,
        stats=stats,
        perms=perms,
        coordinates=coordinates,
        residents=residents,
        trusted=trusted,
        outlaws=outlaws,
        quarters=town_json["quarters"],
        ranks=town_json["ranks"],
    )
    return town_obj
