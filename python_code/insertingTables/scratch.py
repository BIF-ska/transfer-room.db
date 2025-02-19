import json

# Path to your JSON file
json_file_path = r"C:\Users\ska\OneDrive - Brøndbyernes IF Fodbold\Dokumenter\GitHub\transfer-room.db\players_data.json"

def count_unique_teams(file_path):
    """ Quickly count unique teams from the JSON file """
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        # Extract all teams
        teams = set()
        for player in data:
            current_team = player.get('Name')
            if isinstance(current_team, dict):
                team_name = current_team.get('name', 'Unknown Team')
            elif isinstance(current_team, str):
                team_name = current_team
            else:
                team_name = "No Team"

            teams.add(team_name)  # Add to set to ensure uniqueness

        print(f"✅ Total Unique Teams: {len(teams)}")

    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")

if __name__ == "__main__":
    count_unique_teams(json_file_path)
