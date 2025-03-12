import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from models.country import country
from models.team import Teams
from models.competition import Competition
from models.players import Players
from util.database import Database
from util.apiclient import APIClient

SEMAPHORE = asyncio.Semaphore(10)

def cache_db_entries(session):
    return (
        {normalize_name(c.competition_name): c.competition_id for c in session.query(Competition).all()},
        {normalize_name(t.team_name): t.team_id for t in session.query(Teams).all()},
        {normalize_name(c.country_name): c.country_id for c in session.query(country).all()}
    )
 
async def fetch_players(api_client, competition_id):
    return await api_client.fetch_players(competition_id)
 
def bulk_insert_players(session, players, competitions, teams, countries):
    new_players = []

    for player in players:
        if not player.get("Name"):
            continue
        
        tr_id = player["TR_ID"]
        birth_date = datetime.strptime(player["BirthDate"], "%Y-%m-%dT%H:%M:%S") if player.get("BirthDate") else None
        nationality1 = player.get("Nationality1")
        nationality2 = player.get("Nationality2") or ""
        parent_team = (player.get("CurrentTeam") or "Unknown Team").strip()
        competition_name = (player.get("Competition") or "Unknown Competition").strip()
        country_name = player.get("Country")

    
        new_players.append({
            "tr_id": tr_id,
            "player_name": player["Name"],
            "birth_date": datetime.strptime(player["BirthDate"], "%Y-%m-%dT%H:%M:%S") if player.get("BirthDate") else None,
            "first_position": player.get("FirstPosition"),
            "nationality1": player.get("Nationality1"),
            "nationality2": player.get("Nationality2") or "",
            "parent_team": parent_team,
            "competition_id": competitions[competition_name],
            "fk_country_id": countries[country_name],
            "fk_team_id": teams[parent_team],
        })

    if new_players:
        session.bulk_insert_mappings(Players, new_players)
        session.commit()
        print(f"✅ Inserted {len(new_players)} new players.")

def main():
    """Main function to fetch and insert player data."""
    db = Database()
    api_client = APIClient()
    session = db.get_session()
    # Fetch all competitions
    competitions_data = asyncio.run(api_client.fetch_competitions())
 
    if not competitions_data:
        print("❌ No competition data retrieved.")
        return
 
    competitions, teams, countries = cache_db_entries(session)
 
    for competition in competitions_data:
        competition_id = competition["id"]
        players_data = asyncio.run(fetch_players(api_client, competition_id))
 
        if not players_data:
            print(f"❌ No player data for competition {competition_id}.")
            continue
 
        print(f"🚀 Processing {len(players_data)} players for competition {competition_id}...")
        bulk_insert_players(session, players_data, competitions, teams, countries)
 
    session.close()
    print("🎉 All players inserted!")
 
if __name__ == "__main__":
    main()