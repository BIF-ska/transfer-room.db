import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from util.database import Database
from models.players import Players
from models.teamHistory import teamHistory
from datetime import datetime
from util.database import Database


# ✅ JSON file path
json_file = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\excels\players_487.json"

# ✅ Open a database session
db = Database()
session = db.get_session()

try:
    # ✅ Fetch all players to map TR_ID → player_id
    eligible_players = session.query(Players).all()
    tr_id_to_player = {player.tr_id: player.player_id for player in eligible_players if player.tr_id}

    # ✅ Read JSON data
    with open(json_file, "r", encoding="utf-8") as f:
        player_data = json.load(f)

    new_team_history_entries = []

    for player_entry in player_data:
        tr_id = player_entry.get("TR_ID")

        # ✅ Skip if TR_ID is missing or player is not in the database  
        if not tr_id or tr_id not in tr_id_to_player:
            print(f"⚠️ Skipping player TR_ID {tr_id}, not found in Players table.")
            continue  

        player_id = tr_id_to_player[tr_id]  

        # ✅ Extract & parse TeamHistory
        team_history_raw = player_entry.get("TeamHistory")
        if not team_history_raw:
            continue  # No team history, skip

        team_history_list = json.loads(team_history_raw)  # Convert JSON string → list of dicts

        # ✅ Insert each transfer entry
        for transfer in team_history_list:
            from_team = transfer.get("FromTeam", "Unknown")
            to_team = transfer.get("ToTeam", "Unknown")
            start_date = transfer.get("StartDate")
            end_date = transfer.get("EndDate") or None  # Can be empty
            transfer_type = transfer.get("TransferType", "Unknown")
            transfer_fee = transfer.get("TransferFeeEuros")

            # ✅ Convert start_date & end_date to correct format
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None

            # ✅ Check if history already exists (Prevent duplicate entries)
            existing_entry = session.query(teamHistory).filter_by(
                player_id=player_id, from_team=from_team, to_team=to_team, start_date=start_date
            ).first()

            if existing_entry:
                print(f"⚠️ Skipping duplicate transfer for {from_team} → {to_team} (Player ID: {player_id})")
                continue  

            # ✅ Create new TeamHistory record
            new_team_history_entries.append(teamHistory(
                player_id=player_id,
                name=player_entry.get("Name", "Unknown"),
                from_team=from_team,
                to_team=to_team,
                start_date=start_date,
                end_date=end_date,
                transfer_type=transfer_type,
                transfer_fee_euros=float(transfer_fee) if transfer_fee else None,
                created_at=datetime.utcnow()
            ))

    # ✅ Bulk insert if there are new records
    if new_team_history_entries:
        session.bulk_save_objects(new_team_history_entries)
        session.commit()
        print(f"✅ Inserted {len(new_team_history_entries)} new team history records!")

except Exception as e:
    session.rollback()
    print(f"❌ Error inserting team history: {e}")

finally:
    session.close()