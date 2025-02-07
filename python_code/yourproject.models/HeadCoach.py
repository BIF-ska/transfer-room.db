from sqlalchemy import Column, Integer, VARCHAR, Boolean, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Defining the columns dictionary for the HeadCoach model
columns_dict_head_coach = {
    "CoachID": Column(Integer, primary_key=True),
    "Name": Column(String(100)),
    "BirthDate": Column(Date),
    "Nationality1": Column(String(100)),
    "Nationality2": Column(String(100), nullable=True),
    "CurrentTeamID": Column(Integer, ForeignKey('teams.TeamID')),
    "CurrentRole": Column(String(100)),
    "ContractExpiry": Column(Date),
    "AgencyID": Column(Integer, ForeignKey('agencies.AgencyID'))
}

# Defining the HeadCoach model
class HeadCoach(Base):
    __tablename__ = 'HeadCoach'

    CoachID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    BirthDate = Column(Date)
    Nationality1 = Column(String(100))
    Nationality2 = Column(String(100), nullable=True)
    CurrentTeamID = Column(Integer, ForeignKey('teams.TeamID'))
    CurrentRole = Column(String(100))
    ContractExpiry = Column(Date)
    AgencyID = Column(Integer, ForeignKey('agencies.AgencyID'))

    # Relationships
    team = relationship("Teams", back_populates="HeadCoach")
    agency = relationship("Agencies", back_populates="coaches")

    def __repr__(self):
        return f"HeadCoach(CoachID={self.CoachID!r}, Name={self.Name!r}, BirthDate={self.BirthDate!r}, Nationality1={self.Nationality1!r}, Nationality2={self.Nationality2!r}, CurrentTeamID={self.CurrentTeamID!r}, CurrentRole={self.CurrentRole!r}, ContractExpiry={self.ContractExpiry!r}, AgencyID={self.AgencyID!r})"
