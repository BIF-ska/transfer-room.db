import json

# ✅ Path to your JSON file
json_file_path = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\players_data.json"

def load_json_data():
    """Loads player data from JSON file."""
    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"❌ Error loading JSON file: {e}")
        return []

def count_players():
    """Counts total players and players with Agency = 0 or null."""
    players_data = load_json_data()

    if not players_data:
        print("⚠️ No data found in JSON file.")
        return

    total_players = len(players_data)
    players_with_agency = [p for p in players_data if p.get("Agency") not in [None, 0, "null", ""]]
    players_with_no_agency = [p for p in players_data if p.get("Agency") in [None, 0, "null", ""]]

    # ✅ Print the results
    print(f"📌 Total players in JSON: {total_players}")
    print(f"📌 Players with an agency: {len(players_with_agency)}")
    print(f"📌 Players with `Agency = NULL`: {len(players_with_no_agency)}")

if __name__ == "__main__":
    count_players()
