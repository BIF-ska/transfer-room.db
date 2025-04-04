import sys
import asyncio
from pathlib import Path
# Ensure the script can find parent modules
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from sqlalchemy.exc import SQLAlchemyError
from util.apiclient import APIClient
from models.competition import Competition
from models.country import country
from models.team import Teams
from util.database import Database

SEMAPHORE = asyncio.Semaphore(20)

async def fetch_teams(api_client):
    competitions = await api_client.fetch_competitions()
    tasks = [api_client.fetch_players(comp["id"]) for comp in competitions]
    results = await asyncio.gather(*tasks)

    teams = {
        player.get("CurrentTeam", "").strip(): {
            "competition": player.get("Competition", "Unknown").strip(),
            "country": player.get("Country", "Unknown").strip(),
            "tr_id": player.get("TR_ID", -1)
        }
        for players in results for player in players if player.get("CurrentTeam")
    }

    print(f" Extracted {len(teams)} unique teams.")
    return teams

def cache_db(session):
    return {
        "competitions": {c.competition_name: c.competition_id for c in session.query(Competition).all()},
        "countries": {c.country_name: c.country_id for c in session.query(country).all()},
        "teams": {t.team_name for t in session.query(Teams).all()}
    }

def insert_teams(db, teams):
    session = db.get_session()
    cache = cache_db(session)
    new_teams, new_countries, new_competitions = [], [], []

    try:
        for name, data in teams.items():
            if name in cache["teams"]:
                continue  

            country_name = data["country"] or "Unknown Country"  
            comp_name = data["competition"] or "Unknown Competition"
            tr_id = data["tr_id"] if data["tr_id"] != -1 else None 
            division_level = data.get("division_level", 1)  

            if country_name not in cache["countries"]:
                new_country = country(country_name=country_name)
                session.add(new_country)
                session.flush()  
                cache["countries"][country_name] = new_country.country_id

            country_id = cache["countries"][country_name]

            if not country_id:
                print(f"❌ ERROR: country_id is NULL for country: {country_name}.")
                continue  

            if comp_name not in cache["competitions"]:
                new_competition = Competition(
                    tr_id=tr_id, 
                    competition_name=comp_name, 
                    division_level=division_level,  
                    country_id=country_id
                )
                session.add(new_competition)
                session.flush()  
                cache["competitions"][comp_name] = new_competition.competition_id

            competition_id = cache["competitions"][comp_name]

            new_teams.append(Teams(team_name=name, competition_id=competition_id, country_id=country_id))

        session.bulk_save_objects(new_teams)
        session.commit()
        print(f"✅ Inserted {len(new_teams)} new teams!")

    except SQLAlchemyError as e:
        session.rollback()
        print(f"❌ Error inserting teams: {e}")

    finally:
        session.close()

def seed_teams():
    """Fetch and insert teams."""
    db, api_client = Database(), APIClient()

 
    loop = asyncio.get_event_loop()
    teams = loop.run_until_complete(fetch_teams(api_client))

    if not teams:
        print("⚠️ No teams data fetched.")
        return

    insert_teams(db, teams)
    db.dispose_engine()

if __name__ == "__main__":
    seed_teams()