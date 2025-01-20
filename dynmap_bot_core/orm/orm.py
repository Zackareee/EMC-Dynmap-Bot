from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, JSON
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
