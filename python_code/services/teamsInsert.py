import os
import sys 
import asyncio
from pathlib import Path
# Ensure the script can find parent modules
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text  
from sqlalchemy.orm import sessionmaker
from util.apiclient import APIClient
from models.competition import Competition
from models.country import country
from models.team import Teams
from util.database import Database

# ✅ Load environment variables
load_dotenv(override=True)
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Setup Database Connection
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Increase concurrency to fetch multiple competitions in parallel
SEMAPHORE = asyncio.Semaphore(20)  # Increase for parallel API calls

async def fetch_teams_from_players(api_client):
    """Fetch players and extract unique teams using parallel processing."""
    print("📡 Fetching teams from player data...")
    competitions = await api_client.fetch_competitions()
    unique_teams = set()
    team_data_map = {}

    async def fetch_players_for_competition(competition_id):
        async with SEMAPHORE:
            return await api_client.fetch_players(competition_id)

    tasks = [fetch_players_for_competition(comp["id"]) for comp in competitions]
    results = await asyncio.gather(*tasks)

    
    # ✅ Extract teams from players
    for players in results:
        for player in players:
            team_name = player.get("CurrentTeam", "").strip()
            competition_name = player.get("Competition", "").strip()  # ✅ Changed from "competition_id"
            country_name = player.get("Country", "").strip()
            tr_id = player.get("TR_ID")  # ✅ Extract tr_id if available

            if team_name:
                unique_teams.add(team_name)
                team_data_map[team_name] = {
                    "competition_name": competition_name,  # ✅ Changed to match your DB column
                    "country_name": country_name,  # ✅ Changed to match your DB column
                    "tr_id": tr_id  # ✅ Store tr_id
                }

    print(f"✅ Extracted {len(unique_teams)} unique teams from players.")
    return list(unique_teams), team_data_map

def cache_db_entries(db):
    """Preload existing competitions, teams, and countries to reduce queries."""
    competitions = {c.competition_name: c.competition_id for c in db.query(Competition).all()}  # ✅ Corrected
    countries = {c.country_name: c.country_id for c in db.query(country).all()}  # ✅ Corrected
    teams = {t.team_name for t in db.query(Teams).all()}  # Store existing teams as a set
    return competitions, countries, teams

def bulk_insert_teams(unique_teams, competitions, countries, existing_teams, team_data_map):
    """Bulk insert unique teams with correct `competition_id` and `country_id`."""
    db = SessionLocal()
    new_teams = []

    try:
        for team_name in unique_teams:
            if team_name in existing_teams:
                continue  # ✅ Skip existing teams

            team_info = team_data_map.get(team_name, {})
            competition_name = team_info.get("competition_name", "Unknown Competition").strip()
            country_name = team_info.get("country_name", "Unknown Country").strip()
            tr_id = team_info.get("tr_id", None)  # ✅ Get tr_id

            # ✅ Ensure `tr_id` is not NULL
            if tr_id is None:
                print(f"⚠️ Warning: Missing `tr_id` for competition `{competition_name}`. Setting default to -1.")
                tr_id = -1  # ✅ Assign a default value (-1)

            # ✅ Ensure country exists
            if country_name not in countries:
                new_country = country(country_name=country_name)
                db.add(new_country)
                db.flush()
                db.refresh(new_country)
                countries[country_name] = new_country.country_id

            # ✅ Ensure competition exists
            if competition_name not in competitions:
                new_competition = Competition(
                    tr_id=tr_id,  # ✅ Ensures `tr_id` is never NULL
                    competition_name=competition_name,
                    division_level=1,
                    country_id=countries[country_name]
                )
                db.add(new_competition)
                db.flush()
                db.refresh(new_competition)
                competitions[competition_name] = new_competition.competition_id

            # ✅ Add new team to bulk insert list
            new_teams.append(Teams(
                team_name=team_name,
                competition_id=competitions[competition_name],
                country_id=countries[country_name]
            ))

        # ✅ Bulk insert teams
        if new_teams:
            db.bulk_save_objects(new_teams)
            db.commit()
            print(f"✅ Successfully inserted {len(new_teams)} new teams in bulk!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error inserting teams: {e}")

    finally:
        db.close()

def seed_teams():
    """Fetch teams from API and insert into the database."""
    db = SessionLocal()

    api_client = APIClient()

    loop = asyncio.get_event_loop()
    unique_teams, team_data_map = loop.run_until_complete(fetch_teams_from_players(api_client))

    if not unique_teams:
        print("⚠️ No teams data fetched")
        return

    print(f"✅ Extracted {len(unique_teams)} teams from player data.")

    competitions, countries, existing_teams = cache_db_entries(db)

    bulk_insert_teams(unique_teams, competitions, countries, existing_teams, team_data_map)

if __name__ == "__main__":
    seed_teams()