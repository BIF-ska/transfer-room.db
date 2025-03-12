import sys
import asyncio

from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from sqlalchemy import create_engine
from util.apiclient import APIClient
from models.agencies import Agencies  
from util.database import Database
from models.playerAgency import playerAgency
from models.players import Players

def insert_player_agencies(session, players_data):
    """Link players with agencies based on API data."""

    # ✅ Fetch existing Players by TR_ID
    existing_players = {p.tr_id: p.player_id for p in session.query(Players.tr_id, Players.player_id).all()}

    # ✅ Fetch existing Agencies
    existing_agencies = {a.agency_name: a.agency_id for a in session.query(Agencies.agency_name, Agencies.agency_id).all()}

    # ✅ Fetch existing Player-Agency relationships
    existing_links = {(link.player_id, link.agency_id) for link in session.query(playerAgency.player_id, playerAgency.agency_id).all()}

    new_links = []

    for player in players_data:
        tr_id = player.get("TR_ID")
        agency_name = player.get("Agency")

        # ✅ Ensure agency_name is valid before calling .strip()
        if agency_name:
            agency_name = agency_name.strip()
        else:
            continue  # ✅ Skip players with no agency

        # ✅ Ensure player exists in database
        player_id = existing_players.get(tr_id)
        if not player_id:
            print(f"⚠️ Player with TR_ID {tr_id} not found in database. Skipping.")
            continue

        # ✅ Ensure agency exists in database
        agency_id = existing_agencies.get(agency_name)
        if not agency_id:
            new_agency = Agencies(agency_name=agency_name)
            session.add(new_agency)
            session.flush()
            agency_id = new_agency.agency_id
            existing_agencies[agency_name] = agency_id

        # ✅ Insert only if not already linked
        if (player_id, agency_id) not in existing_links:
            new_links.append(playerAgency(player_id=player_id, agency_id=agency_id))
            existing_links.add((player_id, agency_id))

    # ✅ Bulk insert new links
    if new_links:
        session.bulk_save_objects(new_links)
        session.commit()
        print(f"✅ Inserted {len(new_links)} new player-agency relationships.")
    else:
        print("⚠️ No new player-agency relationships to insert.")

def main():
    db = Database()
    api_client = APIClient()
    session = db.get_session()

    players_data = asyncio.run(api_client.fetch_and_save_players())

    if not players_data:
        print("❌ No players fetched.")
        return

    # ✅ Insert player-agency relationships
    insert_player_agencies(session, players_data)

    session.close()
    print("🎉 Player-agency insert complete!")

if __name__ == "__main__":
    main()
