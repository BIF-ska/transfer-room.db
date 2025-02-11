import os
import json
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# Define the Country class
class Country(Base):
    __tablename__ = 'Country'
    
    Country_id = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    
    # Relationships
    competitions = relationship("Competition", back_populates="country")
    teams = relationship("Teams", back_populates="country")

# Define the Competition class
class Competition(Base):
    __tablename__ = 'Competition'

    Competition_id = Column(Integer, primary_key=True)
    Competitionname = Column(String(100), nullable=False)
    divisionLevel = Column(Integer, nullable=False)
    country_fk_id = Column(Integer, ForeignKey("Country.Country_id"))
    
    # Relationships
    country = relationship("Country", back_populates="competitions")
    teams = relationship("Teams", back_populates="competition_team")

# Define the Teams class
class Teams(Base):
    __tablename__ = "Teams"
    
    Team_id = Column(Integer, primary_key=True, autoincrement=True)
    Country_id = Column(Integer, ForeignKey("Country.Country_id"))
    Competition_id = Column(Integer, ForeignKey("Competition.Competition_id"))
    Teamname = Column(String(100))
    
    # Relationships
    country = relationship("Country", back_populates="teams")
    competition_team = relationship("Competition", back_populates="teams")

# --- Seeding Function ---
def seed_teams():
    # --- Load environment variables ---
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ No DATABASE_URL found. Check your .env file.")
        exit(1)
    print("✅ DATABASE_URL loaded successfully.")

    # --- Set up the database engine and session ---
    engine = create_engine(db_url, echo=True)  # echo=True prints SQL statements for debugging.
    engine.dispose()  # Clear any old connections/caches
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # (Optionally create tables if they do not exist)
    # Base.metadata.create_all(engine)

    # --- Authorize and get the token from TransferRoom API ---
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
        exit(1)
    except ValueError as e:
        print(f"Error parsing token: {e}")
        exit(1)

    headers = {"Authorization": f"Bearer {token}"}

    # --- Fetch player data from TransferRoom API ---
    request_url = 'https://apiprod.transferroom.com/api/external/players'
    try:
        r = requests.get(request_url, headers=headers)
        r.raise_for_status()
        json_data = r.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player data: {e}")
        exit(1)

    # --- Debug: Print type and a sample record ---
    print("Type of json_data:", type(json_data))
    if isinstance(json_data, list) and len(json_data) > 0:
        print("Sample record:", json.dumps(json_data[0], indent=4))
    else:
        print("json_data is not a list or is empty.")
        return

    # --- Process JSON Data and Insert into the Database ---
    for player in json_data:
        # Extract nested values from the player record.
        CurrentTeam = player.get('CurrentTeam')
        competition = player.get('Competition')
        country_data = player.get('Country')
        country_name = None  # Initialize country_name

        # Determine the team name.
        if not CurrentTeam:
            team_name = "No Team"
        elif isinstance(CurrentTeam, dict):
            team_name = CurrentTeam.get('name', 'Unknown Team')
        else:
            team_name = str(CurrentTeam)

        print(f"Processing team: {team_name}")

        # Normalize competition value if available.
        if competition:
            if isinstance(competition, dict):
                competition = competition.get('name')
            else:
                competition = str(competition)
            competition = competition.strip()

        # Handle country data.
        if country_data:
            if isinstance(country_data, dict):
                country_name = country_data.get('name')
            else:
                country_name = str(country_data)
            if country_name:
                country_name = country_name.strip()

        # --- Handle Country Record ---
        country_record = None
        if country_name:
            country_record = db.query(Country).filter_by(Name=country_name).first()
            if not country_record:
                country_record = Country(Name=country_name)
                db.add(country_record)
                try:
                    db.commit()  # Commit to generate an ID
                    db.refresh(country_record)
                    print(f"Added Country: {country_record}")
                except Exception as e:
                    db.rollback()
                    print(f"Error committing Country '{country_name}': {e}")
                    continue  # Skip this team if the country cannot be created

        # --- Handle Competition Record ---
        competition_record = None
        if competition:
            competition_record = db.query(Competition).filter_by(Competitionname=competition).first()
            if not competition_record:
                competition_record = Competition(
                    Competitionname=competition,
                    divisionLevel=1,  # or an appropriate default
                    country_fk_id=country_record.Country_id if country_record else None
                )
                db.add(competition_record)
                try:
                    db.commit()  # Commit to generate an ID
                    db.refresh(competition_record)
                    print(f"Added Competition: {competition_record}")
                    print(f"Created Competition with ID: {competition_record.Competition_id}")
                except Exception as e:
                    db.rollback()
                    print(f"Error committing Competition '{competition}': {e}")
                    continue  # Skip this team if the competition cannot be created

        # --- Create and Insert the Team Record ---
        if competition_record and country_record:
            team = Teams(
                Teamname=team_name,
                Competition_id=competition_record.Competition_id,
                Country_id=country_record.Country_id
            )
            db.add(team)
            print(f"Prepared to add Team: {team}")
        else:
            print(f"Skipping team '{team_name}' due to missing Competition or Country record.")

    # Commit all the team records at once.
    try:
        db.commit()
        print("Successfully committed team records.")
    except Exception as e:
        db.rollback()
        print(f"Error during commit of team records: {e}")
    finally:
        db.close()  # Ensure the db session is closed

if __name__ == "__main__":
    seed_teams()
