import os
import json
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
 
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
 
Base = declarative_base()
 
# Database models
class Country(Base):
    __tablename__ = 'Country'
   
    Country_id = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
 
class Competition(Base):
    __tablename__ = 'Competition'
 
    Competition_id = Column(Integer, primary_key=True)
    Competitionname = Column(String(100), nullable=False)
    divisionLevel = Column(Integer, nullable=False, default=1)
    country_fk_id = Column(Integer, ForeignKey("Country.Country_id"))
 
class Teams(Base):
    __tablename__ = "Teams"
 
    Team_id = Column(Integer, primary_key=True, autoincrement=True)
    Teamname = Column(String(100), unique=True)
    Competition_id = Column(Integer, ForeignKey("Competition.Competition_id"))
    Country_id = Column(Integer, ForeignKey("Country.Country_id"))
 
class Players(Base):
    __tablename__ = 'Players'
 
    PlayerID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(100), unique=True)
    BirthDate = Column(DateTime)
    FirstPosition = Column(String(100))
    Nationality1 = Column(String(100))
    Nationality2 = Column(String(100), nullable=True)
    ParentTeam = Column(String(100))
    Rating = Column(Numeric(3, 1))
    Transfervalue = Column(Numeric(10, 2))
    Competition_id = Column(Integer, ForeignKey('Competition.Competition_id'), nullable=False)
    player_Country_id = Column(Integer, ForeignKey('Country.Country_id'), nullable=True)
    TR_ID = Column(Integer, nullable=False)
    fk_players_team = Column(Integer, ForeignKey('Teams.Team_id'), nullable=True)
 
# Database setup
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
def cache_db_entries(db):
    """Preload existing competitions, teams, and countries to reduce queries."""
    competitions = {c.Competitionname: c.Competition_id for c in db.query(Competition).all()}
    teams = {t.Teamname: t.Team_id for t in db.query(Teams).all()}
    countries = {c.Name: c.Country_id for c in db.query(Country).all()}
    return competitions, teams, countries
 
def bulk_insert_players(players_batch, competitions, teams, countries):
    """Efficiently insert players using bulk_insert_mappings."""
    db = SessionLocal()
    new_players = []
   
    try:
        for player in players_batch:
            player_name = player.get("Name")
            if not player_name:
                continue
           
            TR_ID = player.get("TR_ID")
            birth_date = player.get("BirthDate")
            first_position = player.get("FirstPosition")
            nationality1 = player.get("Nationality1")
            nationality2 = player.get("Nationality2")
            parent_team_name = (player.get("CurrentTeam") or "Unknown Team").strip()
            competition_name = (player.get("Competition") or "Unknown Competition").strip()
            country_name = player.get("Country")
            rating = player.get("Rating")
            transfer_value = player.get("xTV")
 
            birth_date = datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S") if birth_date else None
 
            if country_name not in countries:
                country = Country(Name=country_name)
                db.add(country)
                db.commit()
                db.refresh(country)
                countries[country_name] = country.Country_id
            
            
 
            if competition_name not in competitions:
                existing_competition = db.query(Competition).filter_by(Competitionname=competition_name).first()

                if existing_competition:
                    competitions[competition_name] = existing_competition.Competition_id
                else:
                
                
            
    
                   competition = Competition(Competitionname=competition_name, divisionLevel=1)
                   db.add(competition)
                   db.commit()
                   db.refresh(competition)
                   competitions[competition_name] = competition.Competition_id
 
            if parent_team_name not in teams:
                team = Teams(Teamname=parent_team_name, Competition_id=competitions[competition_name], Country_id=countries[country_name])
                db.add(team)
                db.commit()
                db.refresh(team)
                teams[parent_team_name] = team.Team_id
 
            new_players.append({
                "TR_ID": TR_ID,
                "Name": player_name,
                "BirthDate": birth_date,
                "FirstPosition": first_position,
                "Nationality1": nationality1,
                "Nationality2": nationality2,
                "ParentTeam": parent_team_name,
                "Rating": rating,
                "Transfervalue": transfer_value,
                "Competition_id": competitions[competition_name],
                "player_Country_id": countries[country_name],
                "fk_players_team": teams[parent_team_name],
            })
 
        if new_players:
            db.execute(Players.__table__.insert(), new_players)
            db.commit()
 
    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting batch: {e}")
 
    finally:
        db.close()
 
 
def seed_players_from_file():
    """Read players from JSON file and insert them efficiently."""
    file_path = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\players_data.json"
 
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            players_data = json.load(file)
 
        if not players_data:
            print("❌ No player data found in file.")
            return
 
        batch_size = 10000  # Process in larger chunks for efficiency
        players_batches = [players_data[i:i + batch_size] for i in range(0, len(players_data), batch_size)]
 
        print(f"🚀 Processing {len(players_data)} players in {len(players_batches)} batches...")
 
        db = SessionLocal()
        competitions, teams, countries = cache_db_entries(db)
        db.close()
 
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_batch = {executor.submit(bulk_insert_players, batch, competitions, teams, countries): batch for batch in players_batches}
 
            for future in as_completed(future_to_batch):
                future.result()
 
        print("🎉 All players from file processed!")
 
    except Exception as e:
        print(f"❌ Error reading or processing file: {e}")
 
if __name__ == "__main__":
    seed_players_from_file()