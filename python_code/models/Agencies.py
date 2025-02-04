from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from models import Base

columns_dict = {
    "Agency_id": Column(Integer, primary_key=True),
    "Agencyname": Column(String(255)),
    "Agencyverified": Column(Boolean),
    }


class Agencies(Base):
    

    __tablename__ = "agencies"
    Agency_id = Column(Integer, primarykey=True)
    Agencyname = Column(String(255))
    Agencyverified = Column(Boolean)

    # Relationships
    player = relationship("Player")
    agency = relationship("Agency")

    def __repr__(self):
        return f"Agencies(Agency_id={self.Agency_id!r}, Agencyname={self.Agencyname!r}, Agencyverified={self.Agencyverified!r})"