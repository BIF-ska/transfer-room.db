from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base




class Competition(Base):
    __tablename__ = "competition"

    competition_id = Column(Integer, primary_key=True)
    tr_id = Column(Integer)
    competition_name = Column(String(100))
    division_level = Column(Integer)
    country_id = Column(Integer, ForeignKey("country.country_id"))  

   
    #country = relationship("country", back_populates="competitions")


