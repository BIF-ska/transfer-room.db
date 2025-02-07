import os
import glob
import json
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your models
from Players import Players

# Load environment variables (including DATABASE_URL)
load_dotenv()

def seed_players():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("No DATABASE_URL found.")
        return

    # Create engine and session
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # The folder path containing your JSON files
    folder_path = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\python_code\json_data"

    # Use glob to get all .json files in the folder
    json_files = glob.glob(os.path.join(folder_path, "*.json"))
    if not json_files:
        print("No JSON files found in the specified directory.")
        return

    inserted_count = 0  # For debugging: count how many records are added

    for file_path in json_files:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # If the JSON file contains a list of players
        if isinstance(data, list):
            for player_dict in data:
                new_player = Players(
                    Name=player_dict.get("Name"),
                    BirthDate=player_dict.get("BirthDate"),
                    FirstPosition=player_dict.get("FirstPosition"),
                    Nationality1=player_dict.get("Nationality1"),
                    Nationality2=player_dict.get("Nationality2"),
                    ParentTeam=player_dict.get("ParentTeam"),
                    Rating=player_dict.get("Rating"),  # If "Rating" is missing in JSON, this will be None
                    Transfervalue=player_dict.get("xTV")
                )
                session.add(new_player)
                inserted_count += 1

        # If the JSON file contains a single player object
        elif isinstance(data, dict):
            new_player = Players(
                Name=data.get("Name"),
                BirthDate=data.get("BirthDate"),
                FirstPosition=data.get("FirstPosition"),
                Nationality1=data.get("Nationality1"),
                Nationality2=data.get("Nationality2"),
                ParentTeam=data.get("ParentTeam"),
                Rating=data.get("Rating"),  # Corrected: use 'data' instead of 'player_dict'
                Transfervalue=data.get("xTV")
            )
            session.add(new_player)
            inserted_count += 1

        else:
            print(f"Unexpected JSON structure in file: {file_path}")
            continue

    # Commit all changes once all files are processed
    session.commit()
    session.close()
    print(f"All JSON data has been inserted into the Players table. {inserted_count} records added.")

# This block should be at the module level (outside the function)
if __name__ == "__main__":
    seed_players()
