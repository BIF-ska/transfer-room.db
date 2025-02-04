from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, BigInteger
from sqlalchemy.orm import relationship
from models import Base



columns_dict = {
    "Country_id": Column(Integer, primarykey=True),
    "Name": Column(String(255)),
    }

class Country(Base):
    


    __tablename__ = "country"
    Country_id = Column(Integer, primarykey=True)
    Name = Column(String(255))

    # Relationships
    Teams = relationship("Team")
    Country = relationship("Competition")

    def __repr__(self):
        return f"Country(Country_id={self.Country_id!r}, Name={self.Name!r})"
    