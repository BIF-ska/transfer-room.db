import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text
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
    Teamname = Column(String(100), unique=True)
    
    # Relationships
    country = relationship("Country", back_populates="teams")
    competition_team = relationship("Competition", back_populates="teams")

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Database setup
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def cache_db_entries(db):
    """Preload existing competitions, teams, and countries to reduce queries."""
    competitions = {c.Competitionname: c.Competition_id for c in db.query(Competition).all()}
    countries = {c.Name: c.Country_id for c in db.query(Country).all()}
    teams = {t.Teamname for t in db.query(Teams).all()}  # Cache existing teams as a set
    return competitions, countries, teams

def extract_unique_teams(players_data):
    """Extracts a set of unique teams from the players' JSON data."""
    unique_teams = set()
    for player in players_data:
        team_name = player.get("CurrentTeam")
        if team_name:
            unique_teams.add(team_name.strip())  # Store only unique team names
    return list(unique_teams)

def bulk_insert_teams(unique_teams, competitions, countries, existing_teams):
    """Efficiently insert unique teams for SQL Server using MERGE."""
    db = SessionLocal()
    
    try:
        for team_name in unique_teams:
            if team_name in existing_teams:
                continue

            competition_name = "Unknown Competition"
            country_name = "Unknown Country"

            if country_name not in countries:
                country = Country(Name=country_name)
                db.add(country)
                db.flush()
                countries[country_name] = country.Country_id

            if competition_name not in competitions:
                competition = Competition(Competitionname=competition_name, divisionLevel=1)
                db.add(competition)
                db.flush()
                competitions[competition_name] = competition.Competition_id

            sql_query = text("""
            MERGE INTO Teams AS target
            USING (SELECT :team_name AS Teamname, :competition_id AS Competition_id, :country_id AS Country_id) AS source
            ON target.Teamname = source.Teamname
            WHEN NOT MATCHED THEN
                INSERT (Teamname, Competition_id, Country_id)
                VALUES (source.Teamname, source.Competition_id, source.Country_id);
            """)

            db.execute(sql_query, {
                "team_name": team_name,
                "competition_id": competitions[competition_name],
                "country_id": countries[country_name]
            })

        db.commit()
        print(f"✅ Inserted {len(unique_teams)} unique teams!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting teams batch: {e}")

    finally:
        db.close()

def seed_teams_from_file():
    """Extract teams from JSON file and insert unique teams into the database."""
    file_path = r"C:\\Users\\ska\\OneDrive - Brøndbyernes IF Fodbold\\Dokumenter\\GitHub\\transfer-room.db\\players_data.json"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            players_data = json.load(file)

        if not players_data:
            print("❌ No player data found in file.")
            return

        unique_teams = extract_unique_teams(players_data)
        print(f"🚀 Found {len(unique_teams)} unique teams.")

        db = SessionLocal()
        competitions, countries, existing_teams = cache_db_entries(db)
        db.close()

        bulk_insert_teams(unique_teams, competitions, countries, existing_teams)

        print("🎉 All unique teams processed!")

    except Exception as e:
        print(f"❌ Error reading or processing file: {e}")

if __name__ == "__main__":
    seed_teams_from_file()
