from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base



class Agencies(Base):
    __tablename__ = "agencies"

    agency_id = Column(Integer, primary_key=True, autoincrement=True)
    agency_name = Column(String(255), nullable=False, unique=True)
    agency_verified = Column(Boolean, default=False)
