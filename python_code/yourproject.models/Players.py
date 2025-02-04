from sqlalchemy import Column, Integer, VARCHAR, Boolean, ForeignKey, Date, Enum, String
from sqlalchemy.orm import relationship
from models import Base

# Defining the columns dictionary for the Players model
columns_dict_players = {
    "PlayerID": Column(Integer, primary_key=True),
    "Name": Column(String(100)),
    "BirthDate": Column(Date),
    "FirstPosition": Column(String(100)),
    "Nationality1": Column(String(100)),
    "Nationality2": Column(String(100), nullable=True),
    "CurrentTeamID": Column(Integer, ForeignKey('teams.TeamID')),
    "ParentTeam": Column(String(100)),
    "CompetitionID": Column(Integer, ForeignKey('competition.CompetitionID')),
    "TeamID": Column(Integer, ForeignKey('teams.TeamID'))
}

# Defining the Players model
class Players(Base):
    __tablename__ = 'players'

    PlayerID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    BirthDate = Column(Date)
    FirstPosition = Column(String(100))
    Nationality1 = Column(String(100))
    Nationality2 = Column(String(100), nullable=True)
    CurrentTeamID = Column(Integer, ForeignKey('teams.TeamID'))
    ParentTeam = Column(String(100))
    CompetitionID = Column(Integer, ForeignKey('competition.CompetitionID'))
    TeamID = Column(Integer, ForeignKey('teams.TeamID'))

    # Relationships
    team_history = relationship("TeamHistory", back_populates="player")
    current_team = relationship("Teams", foreign_keys=[CurrentTeamID], back_populates="players")

    def __repr__(self):
        return f"Players(PlayerID={self.PlayerID!r}, Name={self.Name!r}, BirthDate={self.BirthDate!r}, FirstPosition={self.FirstPosition!r}, Nationality1={self.Nationality1!r}, Nationality2={self.Nationality2!r}, ParentTeam={self.ParentTeam!r}, CompetitionID={self.CompetitionID!r}, TeamID={self.TeamID!r})"
