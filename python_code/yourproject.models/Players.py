from sqlalchemy import Column, Integer, VARCHAR, Boolean, ForeignKey, Date, Enum, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Defining the columns dictionary for the Players model
columns_dict_players = {
    "PlayerID": Column(Integer, primary_key=True),
    "Name": Column(String(100)),
    "BirthDate": Column(Date),
    "FirstPosition": Column(String(100)),
    "Nationality1": Column(String(100)),
    "Nationality2": Column(String(100), nullable=True),
    "ParentTeam": Column(String(100)),
    "Competition_id": Column(Integer, ForeignKey('Competition.Competition_id')),
    "Team_id": Column(Integer, ForeignKey('teams.Team_id'))
}

class Players(Base):
    __tablename__ = 'Players'

    PlayerID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    BirthDate = Column(Date)
    FirstPosition = Column(String(100))
    Nationality1 = Column(String(100))
    Nationality2 = Column(String(100), nullable=True)
    ParentTeam = Column(String(100))
    Competition_id = Column(Integer, ForeignKey('Competition.Competition_id'))
    Team_id = Column(Integer, ForeignKey('Teams.Team_id'))

    # Relationships
    team_history = relationship("TeamHistory", back_populates="Players")
    team = relationship("Teams", foreign_keys=[Team_id], back_populates="players")
    
    # This relation allows you to access the Country through the Player's Team
    country = relationship("Country", secondary="Teams", back_populates="players")

    def __repr__(self):
        return f"Players(PlayerID={self.PlayerID!r}, Name={self.Name!r}, BirthDate={self.BirthDate!r}, FirstPosition={self.FirstPosition!r}, Nationality1={self.Nationality1!r}, Nationality2={self.Nationality2!r}, ParentTeam={self.ParentTeam!r}, Competition_id={self.Competition_id!r}, Team_id={self.Team_id!r})"

