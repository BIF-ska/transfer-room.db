import sys
import os
import asyncio
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from util.apiclient import APIClient
from models.agencies import Agencies  
from util.database import Database

SEMAPHORE = asyncio.Semaphore(10)  

async def fetch_players_from_api(api_client):
    competitions = await api_client.fetch_competitions()
    all_players = []

    async def fetch_players_for_competition(competition_id):
        
        async with SEMAPHORE:
            return await api_client.fetch_players(competition_id)

    tasks = [fetch_players_for_competition(comp["id"]) for comp in competitions]
    results = await asyncio.gather(*tasks)

    for players in results:
        all_players.extend(players)

    return all_players

def seed_agency():
    load_dotenv()

    db_instance = Database()
    session = db_instance.get_session()

    api_client = APIClient()
    loop = asyncio.get_event_loop()
    players_data = loop.run_until_complete(fetch_players_from_api(api_client))

    if not players_data:
        print("⚠️ No player data fetched. Exiting...")
        return

    existing_agencies = {agency.agency_name for agency in session.query(Agencies.agency_name).all()}
    
    new_agencies = []

    for player in players_data:  
        try:
            player_agency = player.get("Agency")  
            agency_verified = player.get("AgencyVerified", False)  

            agency_verified = True if str(agency_verified).lower() in ["yes", "true", "1"] else False  

            if player_agency and player_agency not in existing_agencies:
                new_agencies.append(Agencies(agency_name=player_agency, agency_verified=agency_verified))
                existing_agencies.add(player_agency)

        except Exception as e:
            print(f"❌ Error processing agency: {e}")

    # ✅ Batch Insert Agencies for Speed
    if new_agencies:
        try:
            session.bulk_save_objects(new_agencies)  # Bulk insert for speed
            session.commit()
            print(f"✅ Successfully inserted {len(new_agencies)} new agencies!")
        except Exception as e:
            
            session.rollback()
    else:
        
    # ✅ Close session properly
     session.close()
     db_instance.close_session()

if __name__ == "__main__":
    seed_agency()