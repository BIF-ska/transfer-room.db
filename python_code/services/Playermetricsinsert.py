import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from util.apiclient import APIClient
from models.playerMetrics import playerMetrics  
from util.database import Database
from models.players import Players
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# JSON file path
json_file = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\excels\players_487.json"

# Initialize database
db = Database()
session = db.get_session()

try:
    # Load JSON data
    with open(json_file, "r", encoding="utf-8") as f:
        player_metrics_data = json.load(f)

    metrics_entries = []
    inserted_tr_ids = set()  

    eligible_players = session.query(Players).filter(Players.competition_id == 40).all()

    tr_id_to_player_id = {player.tr_id: player.player_id for player in eligible_players if player.tr_id}

    for entry in player_metrics_data:
        tr_id = entry.get("TR_ID")  
        if not tr_id or tr_id not in tr_id_to_player_id:
            print(f"⚠️ Skipping entry, no matching PlayerID found for TR_ID {tr_id}")
            continue  

        player_id = tr_id_to_player_id[tr_id]

        existing_metrics = session.query(playerMetrics).filter_by(player_id=player_id).first()
        if existing_metrics:
            print(f"⚠️ Skipping duplicate entry for PlayerID {player_id} (TR_ID: {tr_id})")
            continue 
       
        if tr_id in inserted_tr_ids:
            print(f"⚠️ Skipping duplicate TR_ID {tr_id} from JSON file")
            continue
        inserted_tr_ids.add(tr_id)

      

        metrics = playerMetrics(
            player_id=player_id,
            contract_expiry=entry.get("ContractExpiry"),
            playing_style=entry.get("PlayingStyle"),
            xTV=entry.get("xTV"),
            rating=entry.get("Rating"),
            potential=entry.get("Potential"),
            GBE_result=entry.get("GBEResult"),
            GBE_score=entry.get("GBEScore"),
            base_value=entry.get("BaseValue"),
            estimated_salary=entry.get("EstimatedSalary"),
        )
        metrics_entries.append(metrics)

    if metrics_entries:
        session.bulk_save_objects(metrics_entries)
        session.commit()
        print(f"✅ Inserted {len(metrics_entries)} new player metrics successfully!")
    else:
        print("⚠️ No new player metrics to insert.")

except SQLAlchemyError as e:
    session.rollback()
    print(f"❌ Error inserting player metrics: {e}")

except Exception as e:
    session.rollback()
    print(f"❌ Unexpected Error: {e}")

finally:
    session.close()
    db.dispose_engine()



