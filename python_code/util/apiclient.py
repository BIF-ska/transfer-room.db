import os
import json
import asyncio
import aiohttp
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BASE_URL = os.getenv("base_url")
EMAIL, PASSWORD = os.getenv("email"), os.getenv("password")
AUTH_URL = f"{BASE_URL}?{urlencode({'email': EMAIL, 'password': PASSWORD})}"
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=30)
SEMAPHORE = asyncio.Semaphore(30)

class APIClient:
    """Reusable API client for authentication and data fetching."""

    def __init__(self):
        self.token = None

    async def fetch_api_token(self):
        """Fetch API authentication token (only once)."""
        if self.token:
            return self.token  # Reuse token if already fetched

        async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
            try:
                async with session.post(AUTH_URL) as response:
                    if response.status == 200:
                        self.token = (await response.json()).get("token")
                        print("✅ Token retrieved successfully")
                        return self.token
                    print(f"❌ Authentication failed: {response.status}")
            except Exception as e:
                print(f"⚠️ Error fetching token: {e}")
        return None

    async def fetch_data(self, url):
        """Generic function to fetch data with authentication."""
        token = await self.fetch_api_token()
        if not token:
            return []

        async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
            try:
                async with session.get(url, headers={"Authorization": f"Bearer {token}"}) as response:
                    if response.status == 200:
                        return await response.json()
                    print(f"⚠️ Error fetching data: {response.status}")
            except Exception as e:
                print(f"⚠️ Request failed: {e}")
        return []

    async def fetch_competitions(self):
        """Fetch unique competitions."""
        print("📡 Fetching competitions...")
        data = await self.fetch_data("https://apiprod.transferroom.com/api/external/competitions")
        competitions = {comp["id"]: comp for comp in data}.values()
        print(f"✅ {len(competitions)} competitions retrieved")
        return competitions

    async def fetch_players(self, competition_id):
        """Fetch all players for a competition using pagination."""
        players, offset, last_batch_size = [], 0, -1
        async with SEMAPHORE:
            while True:
                url = f"https://apiprod.transferroom.com/api/external/players?position=0&amount=1000&competitionid={competition_id}&offset={offset}"
                data = await self.fetch_data(url)
                if not data or last_batch_size == len(data):
                    print(f"✅ Finished fetching {len(players)} players for competition {competition_id}")
                    break
                players.extend(data)
                offset += len(data)
                last_batch_size = len(data)
                print(f"🔄 {len(players)} players fetched so far for competition {competition_id}")
        return players

    async def fetch_and_save_players(self, filename="players_data.json"):
        """Fetch players from all competitions and save to a JSON file."""
        competitions = await self.fetch_competitions()
        all_players = []

        for competition in competitions:
            players = await self.fetch_players(competition["id"])
            all_players.extend(players)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(all_players, f, indent=4)
        print(f"✅ Successfully saved {len(all_players)} players to {filename}")
        return all_players

if __name__ == "__main__":
    api_client = APIClient()
    asyncio.run(api_client.fetch_and_save_players())
