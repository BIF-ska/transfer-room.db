import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from util.apiclient import APIClient
from models.playerhistory import playerhistory
from util.database import Database
from models.players import Players
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from util.database import Database


# JSON file path
json_file = r"C:\Users\sad\transferroomDB\transfer-room.db\excels\players_487.json"

# Initialize database
db = Database()
session = db.get_session()



try:
    # 🔥 Step 1: Get Eligible Players (Only for Competition 487)
    eligible_players = session.query(Players).filter(Players.Competition_id == 40).all()

    # 🔥 Step 2: Create Mapping TR_ID → PlayerID + Player Name
    tr_id_to_player = {player.TR_ID: (player.PlayerID, player.Name) for player in eligible_players if player.TR_ID}



    with open(json_file, "r", encoding="utf-8") as f:
        player_data = json.load(f)

    # 🔥 Step 4: Process Each Player Entry
    for player_entry in player_data:
        tr_id = player_entry.get("TR_ID")
        if not tr_id or tr_id not in tr_id_to_player:
            print(f"Skipping player, no matching PlayerID found for TR_ID {tr_id}")
            continue  # Skip players not in our competition

        player_id, player_name = tr_id_to_player[tr_id]  # Get PlayerID & Name from mapping

        # 🔥 Step 5: Extract xTVHistory JSON (It's a string, so convert it)
        xtv_history_raw = player_entry.get("xTVHistory")
        if not xtv_history_raw:
            continue  # Skip if no xTdV history

        xtv_history = json.loads(xtv_history_raw)  # Convert JSON string to a list of dicts

        # 🔥 Step 6: Insert Each xTV History Entry into PlayerHistory Table
        for history_entry in xtv_history:
            new_history = playerhistory(
                tr_id=tr_id,
                year=history_entry["xTVHistory"],
                month=history_entry["xTVHistory"],
                xTV=history_entry["xTV"],
                UpdatedAt=datetime.datetime.utcnow(),
                Name=player_name  # ✅ Now using the correct player name!

            )
            session.add(new_history)

    # 🔥 Commit all transactions
    session.commit()
    print("✅ Successfully inserted xTV history into PlayerHistory table!")

except Exception as e:
    session.rollback()
    print(f"❌ Error: {e}")
finally:
    session.close()
