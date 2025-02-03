from datetime import datetime
from copy import copy
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import BigInteger, Unicode, DateTime, Boolean, Float, Date

Base = declarative_base()

columns_dict = {
    "Id": Column(Integer, primary_key=True),
    "BigId": Column(BigInteger, primary_key=True),  # Changed to BigInteger
    "opta_id": Column(String(length=100), unique=True),
    "string": Column(String(length=100)),
    "short_string": Column(String(length=10)),
    "long_string": Column(Unicode(600)),
    "datetime": Column(DateTime),
    "timestamp": Column(DateTime, default=datetime.utcnow),
    "team_name": Column(String(length=70)),
    "boolean": Column(Boolean, default=False),
    "int": Column(Integer),
    "float": Column(Float),
    "date": Column(Date),
    "big_int": Column(BigInteger),
}

class OptaTeam(Base):
    '''
    This class represents the teams table in the database.

    Attributes:
        id (int): The primary key of the team.
        opta_id (str): The Opta ID of the team.
        name (str): The name of the team.
        short_name (str): The short name of the team.
        official_name (str): The official name of the team.
        code (str): The code of the team.
        area_id (int): The ID of the area of the team.
        team_type_id (int): The ID of the team type of the team.
        status (str): The status of the team.
        city (str): The city of the team.
        address_zip (str): The address zip of the team.
        last_updated (datetime): The last updated timestamp of the team.
        timestamp (datetime): The timestamp of the team.
        area (OptaArea): The area of the team.
        team_type (OptaTeamType): The team type of the team.
        lineups (List[OptaLineup]): The lineups of the team.


    Methods:
     __repr__: Returns the string representation of the team.
    '''

    __tablename__ = "teams"

    __table_args__ = (UniqueConstraint('opta_id'),)

    id = copy(columns_dict["Id"])
    opta_id = copy(columns_dict["opta_id"])
    name = copy(columns_dict["team_name"])
    short_name = copy(columns_dict["team_name"])
    official_name = copy(columns_dict["team_name"])
    code = copy(columns_dict["string"])
    area_id = Column(Integer, ForeignKey("areas.id"))
    team_type_id = Column(Integer, ForeignKey("team_types.id"))
    status = copy(columns_dict["string"])
    city = copy(columns_dict["string"])
    address_zip = copy(columns_dict["string"])
    last_updated = copy(columns_dict["datetime"])
    timestamp = copy(columns_dict["timestamp"])

    area = relationship("OptaArea")
    team_type = relationship("OptaTeamType")
    lineups = relationship("OptaLineup", back_populates="team")

    def __repr__(self):
        return f"Team(id={self.id!r}, name={self.name!r})"