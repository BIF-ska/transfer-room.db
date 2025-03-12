import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Agencies(Base):
    __tablename__ = "Agencies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Agencyname = Column(String(255), nullable=False, unique=True)
    Agencyverified = Column(Boolean, default=False)

