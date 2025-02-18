import os
import json
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
BASE_URL = os.getenv("base_url")
EMAIL = os.getenv("email")
PASSWORD = os.getenv("password")

def fetch_api_token():
    """Fetch API authentication token."""
    auth_url = f"{BASE_URL}?{urlencode({'email': EMAIL, 'password': PASSWORD})}"
    try:
        response = requests.post(auth_url)
        response.raise_for_status()
        return response.json().get("token")
    except requests.RequestException as e:
        print(f"Error during authentication: {e}")
        return None

def fetch_players_data(token):
    """Fetch all player data from API."""
    request_url = 'https://apiprod.transferroom.com/api/external/players?position=0&amount=10000'
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(request_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching player data: {e}")
        return []

def fetch_player_by_name(player_name):
    """Fetch player information by name and return as JSON."""
    token = fetch_api_token()
    if not token:
        return {"error": "Authentication failed"}

    players = fetch_players_data(token)
    
    # Filter player by name
    player_data = next((player for player in players if player["Name"].lower() == player_name.lower()), None)

    if player_data:
        return json.dumps(player_data, indent=4)  # Pretty-print JSON output
    else:
        return {"error": f"No player found with name: {player_name}"}

if __name__ == "__main__":
    player_name = input("Enter the player's name: ").strip()
    player_info = fetch_player_by_name(player_name)
    print(player_info)
