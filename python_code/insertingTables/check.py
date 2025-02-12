import os
import json
from urllib.parse import urlencode
import requests
from dotenv import load_dotenv
python
Copy
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    except requests.exceptions.RequestException as e:
        print(f"Error during authentication: {e}")
        return

    headers = {"Authorization": f"Bearer {token}"}
    request_url = 'https://apiprod.transferroom.com/api/external/players'
    
    total_players = 0
    page = 1

    while True:
        try:
            params = {"page": page, "limit": 100}  # Fetch 100 players per request
            r = requests.get(request_url, headers=headers, params=params)
            r.raise_for_status()
            players_data = r.json()

            if not players_data:  # Stop if API returns an empty list
                break

            total_players += len(players_data)
            print(f"Fetched {len(players_data)} players from page {page}, Total: {total_players}")

            page += 1

        except requests.exceptions.RequestException as e:
            print(f"Error fetching player data: {e}")
            break

    print(f"Total players available in API: {total_players}")

if __name__ == "__main__":
    check_api_player_count()
