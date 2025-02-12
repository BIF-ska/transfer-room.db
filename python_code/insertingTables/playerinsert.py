import os
import json
from urllib.parse import urlencode
from datetime import datetime
import requests
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Numeric, DATE
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

# --- Database Models (ingen ændringer her) ---

def get_api_token():
    """Henter API-token for authentication"""
    email = 'dst@brondby.com'
    password = 'BifAdmin1qazZAQ!TransferRoom'
    base_url = "https://apiprod.transferroom.com/api/external/login"
    params = {'email': email, 'password': password}
    auth_url = f"{base_url}?{urlencode(params)}"

    try:
        r = requests.post(auth_url)
        r.raise_for_status()
        token_json_data = r.json()
        token = token_json_data.get('token')
        if not token:
            raise ValueError("Token not found in API response.")
        print("✅ Authentication successful!")
        return token
    except requests.exceptions.RequestException as e:
        print(f"❌ Error during authentication: {e}")
        return None

def fetch_all_players(token):
    """Henter alle spillere fra API'et og håndterer pagination"""
    headers = {"Authorization": f"Bearer {token}"}
    request_url = "https://apiprod.transferroom.com/api/external/players"

    all_players = []
    page = 1
    total_pages = 1  # Antager 1 side som default

    while page <= total_pages:
        try:
            response = requests.get(f"{request_url}?page={page}", headers=headers)
            response.raise_for_status()
            data = response.json()

            # Debugging: Se hvordan API'et returnerer data
            print("API Response Type:", type(data))
            print("API Response Preview:", json.dumps(data[:5], indent=4))  # Udskriver de første 5 spillere

            # Hvis API'et returnerer en **liste**, så er det alle spillere
            if isinstance(data, list):
                players = data
                total_pages = 1  # Hvis der ikke er pagination, kører vi kun én gang
            elif isinstance(data, dict) and "players" in data:
                players = data["players"]
                total_pages = data.get("totalPages", 1)  # Henter pagination-info, hvis den findes
            else:
                print("❌ Uventet API-response format!")
                return []

            all_players.extend(players)
            print(f"✅ Fetched page {page}, {len(players)} players found.")

            page += 1  # Gå til næste side

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching player data on page {page}: {e}")
            break

    print(f"✅ Total players fetched: {len(all_players)}")
    return all_players


def seed_players():
    """Henter spillere fra API og indsætter dem i databasen"""
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ No DATABASE_URL found.")
        return

    engine = create_engine(db_url, echo=True)
    engine.dispose()

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    token = get_api_token()
    if not token:
        return

    players_data = fetch_all_players(token)
    if not players_data:
        print("❌ No player data received from API.")
        return

    for player in players_data:
        try:
            player_name = player.get("Name")
            birth_date = player.get("BirthDate")
            first_position = player.get("FirstPosition")
            nationality1 = player.get("Nationality1")
            nationality2 = player.get("Nationality2")
            parent_team_name = player.get("CurrentTeam")
            competition_name = player.get("Competition", "").strip()
            rating = player.get("Rating")
            transfer_value = player.get("xTV")

            # Håndterer Competition-feltet korrekt
            competition_name = player.get("Competition")
            if competition_name is None:
                print(f"⚠️ Missing competition for player: {player_name}")
                competition_name = "Unknown"
            else:
                competition_name = str(competition_name).strip()

            # Håndterer CurrentTeam-feltet korrekt
            parent_team_name = player.get("CurrentTeam")
            if parent_team_name is None:
                print(f"⚠️ Missing team for player: {player_name}")
                parent_team_name = "Unknown"
            else:
                parent_team_name = str(parent_team_name).strip()

            # Konverter fødselsdato
            birth_date = datetime.strptime(birth_date, "%Y-%m-%dT%H:%M:%S") if birth_date else None

            print(f"INSERT Data: {player_name}, Team={parent_team_name}, Competition={competition_name}")

        except Exception as e:
            print(f"❌ Error inserting player {player_name}: {e}")

    db.close()

if __name__ == "__main__":
    seed_players()
