import os
import json
from urllib.parse import urlencode
from datetime import datetime
import requests
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric, DATE, Date, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Agencies(Base):
    __tablename__ = "Agencies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    Agencyname = Column(String(255), nullable=False, unique=True)
    Agencyverified = Column(Boolean, default=False)

    # Relationships
    player = relationship("Player")
    agency = relationship("Agency")
    coaches = relationship("HeadCoach", back_populates="agency")

class HeadCoach(Base):
    __tablename__ = 'HeadCoach'

    CoachID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    BirthDate = Column(Date)
    Nationality1 = Column(String(100))
    Nationality2 = Column(String(100), nullable=True)
    CurrentRole = Column(String(100))
    ContractExpiry = Column(Date)
    fk_Head_Coach = Column(Integer, ForeignKey('agencies.AgencyID'))

    # Relationships
    agency = relationship("Agencies", back_populates="coaches")

# --- Seeding Function ---
def seed_headcoach():
    # --- Load environment variables ---
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ No DATABASE_URL found. Check your .env file.")
        return
    print("✅ DATABASE_URL loaded successfully.")

    # --- Set up the database engine and session ---
    engine = create_engine(db_url, echo=True)  # echo=True prints SQL statements for debugging.
    engine.dispose()  # Clear any old connections/caches
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    email = 'dst@brondby.com'
    password = 'BifAdmin1qazZAQ!TransferRoom'
    base_url = "https://apiprod.transferroom.com/api/external/login"
    params = {'email': email, 'password': password}
    auth_url = f"{base_url}?{urlencode(params)}"

    try:
        r = requests.post(auth_url)
        r.raise_for_status()
        token_json_data = r.json()
        token = token_json_data.get('token')
        if not token:
            raise ValueError("Token not found in the API response.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during authentication: {e}")
        return
    except ValueError as e:
        print(f"❌ Error parsing token: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

   # --- Fetch HeadCoach Data ---
    request_url = 'https://apiprod.transferroom.com/api/external/coaches'  # Double-check API URL
    try:
        r = requests.get(request_url, headers=headers)
        r.raise_for_status()
        headcoach_data = r.json()

        # Print out the structure of the fetched data for debugging
        print(json.dumps(headcoach_data, indent=4))  # See what data looks like
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching head coach data: {e}")
        return

   
    
    
    
seed_headcoach()