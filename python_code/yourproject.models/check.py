import os
import json
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv

def check_api_player_count():
    load_dotenv()

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

    except requests.exceptions.RequestException as e:
        print(f"❌ Error during authentication: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}
    request_url = 'https://apiprod.transferroom.com/api/external/players'

    try:
        r = requests.get(request_url, headers=headers)
        r.raise_for_status()
        players_data = r.json()

        # Tæl hvor mange spillere der er i dataen
        num_players = len(players_data)

        print(f"✅ API returned {num_players} players.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching player data: {e}")

# Kald funktionen
check_api_player_count()

   
    
 