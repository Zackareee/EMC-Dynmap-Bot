import sqlalchemy as sa
import pandas as pd

from typing import Optional, List
from dataclasses import dataclass
from sqlalchemy import String, Float, LargeBinary
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, ForeignKey, String, Text, JSON
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Base(DeclarativeBase):
    pass


class Town(Base):
    __tablename__ = "town"

    uuid = Column(String, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    coordinates = Column(JSON, nullable=False)

    # Relationship to the Player table
    players = relationship("Player", back_populates="town")


class Player(Base):
    __tablename__ = "player"

    uuid = Column(String, primary_key=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    town_id = Column(String, ForeignKey("town.uuid"))

    # Relationship to the Town table
    town = relationship("Town", back_populates="players")

@dataclass
class TownCoordinates:
    coordinates: list[list[int,int]]

def unpack_town_coordinates(town_json) -> [float]:
    coordinates = town_json["coordinates"]["townBlocks"],
    return coordinates


def unpack_town_response(town_json) -> Town:
    town_obj: Town = Town(
        name=town_json["name"],
        uuid=town_json["uuid"],
        coordinates=town_json["coordinates"]["townBlocks"],
    )
    return town_obj
