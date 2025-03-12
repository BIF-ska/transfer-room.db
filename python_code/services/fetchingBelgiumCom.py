import os
import json
import asyncio
import aiohttp
from urllib.parse import urlencode
from dotenv import load_dotenv
from aiohttp import ClientTimeout

# ✅ Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# ✅ API settings
MAX_CONCURRENT_REQUESTS = 5  # Limit concurrent requests
REQUEST_TIMEOUT = ClientTimeout(total=30)  # Set timeout
COMPETITION_ID = 487  # Target Competition (First Division A)

async def fetch_api_token():
    """Fetch API authentication token asynchronously."""
    email = os.getenv("email")
    password = os.getenv("password")
    base_url = os.getenv("base_url")
    auth_url = f"{base_url}?{urlencode({'email': email, 'password': password})}"

    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
        try:
            async with session.post(auth_url) as response:
                response.raise_for_status()
                token_data = await response.json()
                return token_data.get("token")
        except aiohttp.ClientError as e:
            print(f"❌ Error during authentication: {e}")
            return None

async def fetch_data(session, token, url, entity_name):
    """Generic function to fetch data from a given URL."""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        async with session.get(url, headers=headers, timeout=REQUEST_TIMEOUT) as response:
            response.raise_for_status()
            data = await response.json()
            print(f"✅ Successfully fetched {len(data)} {entity_name}")
            return data
    except aiohttp.ClientError as e:
        print(f"❌ Error fetching {entity_name}: {e}")
        return []

async def fetch_players_for_competition(session, token, competition_id):
    """Fetch all players from a specific competition (using pagination)."""
    all_players = []
    offset = 0  # Start from the first player
    last_batch_size = -1  # Track batch size to prevent infinite loops

    while True:
        request_url = f"https://apiprod.transferroom.com/api/external/players?position=0&amount=1000&competitionid={competition_id}&offset={offset}"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            async with session.get(request_url, headers=headers, timeout=REQUEST_TIMEOUT) as response:
                response.raise_for_status()
                json_data = await response.json()

                players = json_data if isinstance(json_data, list) else json_data.get("players", [])

                if not players:
                    print(f"✅ Finished fetching players for competition {competition_id}. Total: {len(all_players)}")
                    break  # Stop fetching when no more players

                all_players.extend(players)
                offset += len(players)  # Move offset for next batch

                # Stop if API keeps returning the same batch size
                if last_batch_size == len(players):
                    print(f"⚠️ Possible pagination loop detected. Stopping at {offset} players.")
                    break

                last_batch_size = len(players)  # Update last batch size
                print(f"Fetched {len(players)} players, total so far: {len(all_players)}")

        except asyncio.TimeoutError:
            print(f"⏳ Timeout fetching players for competition {competition_id}. Retrying...")
            await asyncio.sleep(2)  # Wait and retry
        except aiohttp.ClientError as e:
            print(f"❌ Error fetching players for competition {competition_id}: {e}")
            break  # Stop fetching on error

    return all_players

async def fetch_data_for_487():
    """Fetch players and coaches for Competition ID 487 (First Division A) and save to JSON."""
    token = await fetch_api_token()
    if not token:
        print("❌ Failed to authenticate.")
        return

    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
        # ✅ Fetch Players
        players_487 = await fetch_players_for_competition(session, token, COMPETITION_ID)

        # ✅ Fetch Coaches (All Available)
        coaches_url = "https://apiprod.transferroom.com/api/external/coaches"
        coaches_487 = await fetch_data(session, token, coaches_url, "coaches")

    print(f"🎯 Total Players Fetched for First Division A: {len(players_487)}")
    print(f"🎯 Total Coaches Fetched: {len(coaches_487)}")

    # ✅ Save Players to JSON
    with open("players_487.json", "w", encoding="utf-8") as f:
        json.dump(players_487, f, indent=4, ensure_ascii=False)
    print("✅ Player data saved to players_487.json")

    # ✅ Save Coaches to JSON
    with open("coaches_487.json", "w", encoding="utf-8") as f:
        json.dump(coaches_487, f, indent=4, ensure_ascii=False)
    print("✅ Coach data saved to coaches_487.json")

if __name__ == "__main__":
    asyncio.run(fetch_data_for_487())
