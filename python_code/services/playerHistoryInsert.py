import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from util.apiclient import APIClient
from models.playerhistory import playerhistory
from util.database import Database
from models.players import Players
from models.team import Teams
from models.country import country
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
from util.database import Database



json_file = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\excels\players_487.json"

db = Database()
session = db.get_session()

try:
    
    eligible_players = session.query(Players).filter(Players.competition_id == 40).all()
    tr_id_to_player_id = {player.tr_id: player.player_id for player in eligible_players if player.tr_id}

    team_cache = {t.team_name: t.team_id for t in session.query(Teams).all()}
    country_cache = {c.country_name: c.country_id for c in session.query(country).all()}

    with open(json_file, "r", encoding="utf-8") as f:
        player_data = json.load(f)

    new_players = []
    new_history_entries = []

    for player_entry in player_data:
        tr_id = player_entry.get("TR_ID")
        player_name = player_entry.get("Name", "Unknown Player")
        country_name = player_entry.get("Country", "Unknown Country")
        team_name = player_entry.get("ParentTeam", "Unknown Team")

        if not tr_id:
            print(f"⚠️ Skipping player with missing TR_ID: {player_name}")
            continue  

        if country_name not in country_cache:
            print(f"🆕 Adding missing country: {country_name}")
            new_country = country(country_name=country_name)
            session.add(new_country)
            session.flush()
            country_cache[country_name] = new_country.country_id

        fk_country_id = country_cache[country_name]

        if team_name not in team_cache:
            print(f"🆕 Adding missing team: {team_name}")
            new_team = Teams(team_name=team_name)
            session.add(new_team)
            session.flush()
            team_cache[team_name] = new_team.team_id

        fk_team_id = team_cache[team_name]

        if tr_id not in tr_id_to_player_id:
            print(f"🆕 Adding missing player: {player_name} (TR_ID: {tr_id})")

            new_player = Players(
                tr_id=tr_id,
                player_name=player_name,
                birth_date=player_entry.get("BirthDate"),
                first_position=player_entry.get("FirstPosition"),
                nationality1=player_entry.get("Nationality1"),
                nationality2=player_entry.get("Nationality2"),
                parent_team=team_name,
                competition_id=40,
                fk_team_id=fk_team_id,
                fk_country_id=fk_country_id
            )
            session.add(new_player)
            session.flush() 
            tr_id_to_player_id[tr_id] = new_player.player_id  

       
        player_id = tr_id_to_player_id.get(tr_id)
        if not player_id:
            print(f"⚠️ Skipping history for TR_ID {tr_id}: No player_id found")
            continue 

     
        xtv_history_raw = player_entry.get("xTVHistory")
        if not xtv_history_raw:
            continue  

        xtv_history = json.loads(xtv_history_raw)

        for history_entry in xtv_history:
            new_history = playerhistory(
                player_id=player_id,  
                year=history_entry["year"],
                month=history_entry["month"],
                xTV=history_entry["xTV"],
                UpdatedAt=datetime.datetime.utcnow(),
                Name=player_name  # ✅ Now using the correct player name!

            )
            new_history_entries.append(new_history)

    session.commit()  

    if new_history_entries:
        session.bulk_save_objects(new_history_entries)
        session.commit()
        print(f"✅ Successfully inserted {len(new_history_entries)} player history records!")
    else:
        print("⚠️ No new player history records to insert.")

except Exception as e:
    session.rollback()
    print(f"❌ Error: {e}")

finally:
    session.close()