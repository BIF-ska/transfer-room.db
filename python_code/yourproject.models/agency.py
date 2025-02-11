import os
import json
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
 
Base = declarative_base()
 
class Agencies(Base):
    __tablename__ = "Agencies"
 
    id = Column(Integer, primary_key=True, autoincrement=True)
    Agencyname = Column(String(255), nullable=False, unique=True)
    Agencyverified = Column(Boolean, default=False)
 
    # Relationships
    players = relationship("Player", back_populates="agency")  # Sørg for, at Player eksisterer






def seed_agency():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found.")
        return

    engine = create_engine(db_url, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Authenticate with TransferRoom API
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
        print(f"Error during authentication: {e}")
        return
    except ValueError as e:
        print(f"Error parsing token: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    # Fetch player data from TransferRoom API
    request_url = 'https://apiprod.transferroom.com/api/external/players'
    try:
        r = requests.get(request_url, headers=headers)
        r.raise_for_status()
        json_data = r.json()
        
        # Print the JSON response to the terminal
        print(json.dumps(json_data, indent=4))
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player data: {e}")
        return

if __name__ == "__main__":
    seed_agency()
