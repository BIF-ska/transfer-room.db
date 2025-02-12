import os
import json
from urllib.parse import urlencode
from datetime import datetime
import requests
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric, DATE
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Country(Base):
    __tablename__ = 'Country'
    
    Country_id = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    
    competitions = relationship("Competition", back_populates="country")
    teams = relationship("Teams", back_populates="country")

class Competition(Base):
    __tablename__ = 'Competition'

    Competition_id = Column(Integer, primary_key=True)
    Competitionname = Column(String(100), nullable=False)
    divisionLevel = Column(Integer, nullable=False)
    country_fk_id = Column(Integer, ForeignKey("Country.Country_id"))
    
    country = relationship("Country", back_populates="competitions")
    teams = relationship("Teams", back_populates="competition_team")

class Teams(Base):
    __tablename__ = "Teams"

    Team_id = Column(Integer, primary_key=True, autoincrement=True)
    Teamname = Column(String(100))
    Competition_id = Column(Integer, ForeignKey("Competition.Competition_id"))
    Country_id = Column(Integer, ForeignKey("Country.Country_id"))
    
    country = relationship("Country", back_populates="teams")
    competition_team = relationship("Competition", back_populates="teams")
    players = relationship("Players", back_populates="team")

class Players(Base):
    __tablename__ = 'Players'

    PlayerID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    BirthDate = Column(DateTime)
    FirstPosition = Column(String(100))
    Nationality1 = Column(String(100))
    Nationality2 = Column(String(100), nullable=True)
    ParentTeam = Column(String(100))
    Rating = Column(Numeric(3, 1))
    Transfervalue = Column(Numeric(10, 2))
    Competition_id = Column(Integer, ForeignKey('Competition.Competition_id'), nullable=True)
    fk_players_team = Column(Integer, ForeignKey('Teams.Team_id'), nullable=True)

    team = relationship("Teams", foreign_keys=[fk_players_team], back_populates="players")

def seed_players():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found.")
        return

    engine = create_engine(db_url, echo=True)
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
        print(f"Error during authentication: {e}")
        return
    except ValueError as e:
        print(f"Error parsing token: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}

    request_url = 'https://apiprod.transferroom.com/api/external/players'
    try:
        r = requests.get(request_url, headers=headers)
        r.raise_for_status()
        players_data = r.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching player data: {e}")
        return

    for player in players_data:
        try:
            player_name = player.get("Name")
            birth_date = player.get("BirthDate")
            first_position = player.get("FirstPosition")
            nationality1 = player.get("Nationality1")
            nationality2 = player.get("Nationality2")
            parent_team_name = player.get("CurrentTeam")
            competition_name = player.get("Competition").strip()
            rating = player.get("Rating")
            transfer_value = player.get("xTV")

            if not parent_team_name or not competition_name:
                print(f"Skipping player {player_name} due to missing team or competition.")
                continue

            birth_date = datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S") if birth_date else None

            competition = db.query(Competition).filter_by(Competitionname=competition_name).first()
            if not competition:
                print(f"Creating new competition: {competition_name}")
                competition = Competition(Competitionname=competition_name, divisionLevel=4)
                db.add(competition)
                db.commit()
                db.refresh(competition)

            team = db.query(Teams).filter_by(Teamname=parent_team_name).first()
            if not team:
                team = Teams(Teamname=parent_team_name, Competition_id=competition.Competition_id)
                db.add(team)
                db.commit()
                db.refresh(team)
                print(f"INSERT Data: Name={player_name}, BirthDate={birth_date}, FirstPosition={first_position}, "
      f"Nationality1={nationality1}, Nationality2={nationality2}, ParentTeam={parent_team_name}, "
      f"Rating={rating}, TransferValue={transfer_value}, CompetitionID={competition.Competition_id}, "
      f"TeamID={team.Team_id}")


            new_player = Players(
                Name=player_name,
                BirthDate=birth_date,
                FirstPosition=first_position,
                Nationality1=nationality1,
                Nationality2=nationality2,
                ParentTeam=parent_team_name,
                Rating=rating,
                Transfervalue=transfer_value,
                Competition_id=competition.Competition_id,
                fk_players_team=team.Team_id,
            )

            db.add(new_player)
            db.commit()
            print(f"Successfully inserted: {player_name}")

        except Exception as e:
            db.rollback()
            print(f"Error inserting player {player_name}: {e}")

    db.close()

if __name__ == "__main__":
    seed_players()
