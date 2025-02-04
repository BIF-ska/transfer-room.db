from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship
from models import Base


columns_dict = {
    "Competition_id": Column(Integer, primarykey=True),
    "Competitionname": Column(String(100)),
    "Country_ID": Column(Integer, ForeignKey=True),
    }

class Competition(Base):
   
    __tablename__ = "competetion"
    Competition_id = Column(Integer, primarykey=True)
    Competitionname = Column(String(100))
    Country_ID = Column(Integer, ForeignKey("country.id"))

    # Relationships
    Competition = relationship("Competition")
    team = relationship("Team")

    def __repr__(self):
        return f"Competition(Competition_id={self.Competition_id!r}, Competitionname={self.Competitionname!r}, Country_ID={self.Country_ID!r})"
