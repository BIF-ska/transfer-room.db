import os
import json
import pandas as pd
import pyodbc
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ Connect to the Database
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# ✅ Load JSON Data
json_file = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\excels\players_487.json"

with open(json_file, "r", encoding="utf-8") as file:
    players_data = json.load(file)

# ✅ Insert or Update Players in the Database
for player in players_data:
    tr_id = player.get("TR_ID")
    name = player.get("Name")
    birth_date = player.get("BirthDate")
    nationality1 = player.get("Nationality1")
    nationality2 = player.get("Nationality2")
    parent_team = player.get("ParentTeam")
    rating = player.get("Rating")
    transfer_value = player.get("xTV")  # Assuming xTV is the transfer value
    competition_id = 487  # Hardcoded since we know it's First Division A
    player_country_id = None  # Adjust logic if needed
    fk_players_team = None  # Adjust logic if needed

    # ✅ Check if Player Exists
    existing_player = db.execute(
        text("SELECT PlayerID FROM Players WHERE TR_ID = :tr_id"),
        {"tr_id": tr_id}
    ).fetchone()

    if existing_player:
        print(f"🔄 Updating Player: {name} (TR_ID: {tr_id})")
        db.execute(
            text("""
            UPDATE Players 
            SET Name=:name, BirthDate=:birth_date, FirstPosition=:first_position, 
                Nationality1=:nationality1, Nationality2=:nationality2, 
                ParentTeam=:parent_team, Rating=:rating, 
                Transfervalue=:transfer_value, Competition_id=:competition_id 
            WHERE TR_ID=:tr_id
            """),
            {
                "name": name,
                "birth_date": birth_date,
                "first_position": player.get("FirstPosition"),
                "nationality1": nationality1,
                "nationality2": nationality2,
                "parent_team": parent_team,
                "rating": rating,
                "transfer_value": transfer_value,
                "competition_id": competition_id,
                "tr_id": tr_id
            }
        )
    else:
        print(f"✅ Inserting New Player: {name} (TR_ID: {tr_id})")
        db.execute(
            text("""
            INSERT INTO Players (Name, BirthDate, FirstPosition, Nationality1, Nationality2, 
                ParentTeam, Rating, Transfervalue, Competition_id, TR_ID) 
            VALUES (:name, :birth_date, :first_position, :nationality1, :nationality2, 
                :parent_team, :rating, :transfer_value, :competition_id, :tr_id)
            """),
            {
                "name": name,
                "birth_date": birth_date,
                "first_position": player.get("FirstPosition"),
                "nationality1": nationality1,
                "nationality2": nationality2,
                "parent_team": parent_team,
                "rating": rating,
                "transfer_value": transfer_value,
                "competition_id": competition_id,
                "tr_id": tr_id
            }
        )

# ✅ Commit Changes & Close Connection
db.commit()
db.close()

print("🎯 Players inserted/updated successfully!")
