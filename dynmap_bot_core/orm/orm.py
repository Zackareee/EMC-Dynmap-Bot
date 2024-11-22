import sqlalchemy
import pandas as pd

from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass


class Town(Base):
    __tablename__ = "Town"
    uuid: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    board: Mapped[str] = mapped_column(String(30))
    founder: Mapped[str] = mapped_column(String(30))
    wiki: Mapped[str] = mapped_column(String(30))
    nation: Mapped[str] = mapped_column(String(30))
    timestamps: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(30))
    stats: Mapped[str] = mapped_column(String(30))
    perms: Mapped[str] = mapped_column(String(30))
    coordinates: Mapped[str] = mapped_column(String(30))
    residents: Mapped[str] = mapped_column(String(30))
    trusted: Mapped[str] = mapped_column(String(30))
    outlaws: Mapped[str] = mapped_column(String(30))
    quarters: Mapped[str] = mapped_column(String(30))
    ranks: Mapped[str] = mapped_column(String(30))
    mayor: Mapped[str] = mapped_column(sqlalchemy.ForeignKey("Player.uuid"))  # Correct foreign key
    mayor_id: Mapped["Player"] = sqlalchemy.orm.relationship("Player", back_populates="towns")


class Player(Base):
    __tablename__ = "Player"
    uuid: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    title: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    formattedName: Mapped[str] = mapped_column(String(30))
    about: Mapped[dict[str,str]] = mapped_column(String(30))
    timestamps: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(30))
    stats: Mapped[str] = mapped_column(String(30))
    perms: Mapped[str] = mapped_column(String(30))
    ranks: Mapped[str] = mapped_column(String(30))
    friends: Mapped[str] = mapped_column(String(30))
    towns: Mapped[list["Town"]] = sqlalchemy.orm.relationship("Town", back_populates="mayor_id")  # Back-reference


dbEngine = sqlalchemy.create_engine(r'sqlite:///database.db') # ensure this is the correct path for the sqlite file.
session = sqlalchemy.orm.Session(dbEngine)
stmt = sqlalchemy.select(Town)
result = session.execute(stmt).all()
for town in result:
    town = town

val = pd.read_sql('select * from Town',dbEngine)
pass


