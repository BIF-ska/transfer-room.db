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
import unicodedata
 
 
SEMAPHORE = asyncio.Semaphore(30)
 
 
def normalize_name(name):
    return unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII').strip()
 
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
 
    existing_tr_ids = {tr_id for (tr_id,) in session.query(Players.tr_id).all()}
 
    for player in players:
        if not player.get("Name"):
            continue  
 
        tr_id = player["TR_ID"]
 
        if tr_id in existing_tr_ids:
            print(f"⚠️ Skipping duplicate player with TR_ID: {tr_id}")
            continue
 
        competition_name = normalize_name(player.get("Competition") or "Unknown Competition")
        parent_team = normalize_name(player.get("CurrentTeam") or "Unknown Team")
        country_name = normalize_name(player.get("Country") or "Unknown Country")
 
        if competition_name not in competitions:
            print(f"⚠️ WARNING: Competition '{competition_name}' not found. Adding it now...")
            if country_name not in countries:
                new_country = country(country_name=country_name)
                session.add(new_country)
                session.flush()
                countries[country_name] = new_country.country_id  
 
            new_competition = Competition(
                competition_name=competition_name,
                tr_id=tr_id,
                division_level=1,  
                country_id=countries[country_name]
            )
            session.add(new_competition)
            session.flush()
            competitions[competition_name] = new_competition.competition_id  
 
        if parent_team not in teams:
            print(f"⚠️ WARNING: Team '{parent_team}' not found. Adding it now...")
            new_team = Teams(team_name=parent_team, competition_id=competitions[competition_name], country_id=countries[country_name])
            session.add(new_team)
            session.flush()
            teams[parent_team] = new_team.team_id  
 
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
        print(f"✅ Inserted {len(new_players)} new players (excluding duplicates).")
 
def run_player_update():
    """Main function to fetch and insert player data."""
    db = Database()
    api_client = APIClient()
    session = db.get_session()
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
        run_player_update()
