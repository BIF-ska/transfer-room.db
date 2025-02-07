from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger, Date, Enum
from sqlalchemy.orm import relationship
from datetime import datetime


# Defining the columns dictionary for the TeamHistory model
columns_dict_team_history = {
    "TeamHistory_ID": Column(Integer, primary_key=True),
    "PlayerID": Column(Integer, ForeignKey('players.PlayerID')),
    "TeamID": Column(Integer, ForeignKey('teams.TeamID')),
    "StartDate": Column(Date),
    "EndDate": Column(Date),
    "EntityType": Column(Enum('Player', 'Coach', name='entity_type_enum')),
}

# Defining the TeamHistory model
class TeamHistory(Base):
    __tablename__ = 'TeamHistory'

    TeamHistory_ID = Column(Integer, primary_key=True)
    PlayerID = Column(Integer, ForeignKey('players.PlayerID'))
    TeamID = Column(Integer, ForeignKey('teams.TeamID'))
    StartDate = Column(Date)
    EndDate = Column(Date)
    EntityType = Column(Enum('Player', 'Coach', name='entity_type_enum'))

    player = relationship("Players", back_populates="team_history")
    team = relationship("Teams", back_populates="team_history")

    def __repr__(self):
        return f"TeamHistory(TeamHistory_ID={self.TeamHistory_ID!r}, PlayerID={self.PlayerID!r}, TeamID={self.TeamID!r}, StartDate={self.StartDate!r}, EndDate={self.EndDate!r}, EntityType={self.EntityType!r})"


