import os
import json
import aiohttp
import asyncio
import time
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_BASE_URL = os.getenv("base_url")
EMAIL = os.getenv("email")
PASSWORD = os.getenv("password")

# Configuration
LIMIT_PER_REQUEST = 1000  # Maximum players per request
MAX_CONCURRENT_REQUESTS = 20  # Number of simultaneous requests
RATE_LIMIT_SLEEP = 60  # Wait time (seconds) if rate-limited

async def fetch_api_token():
    """Authenticate and fetch API token."""
    if not API_BASE_URL or not EMAIL or not PASSWORD:
        print("❌ Missing API credentials in .env file.")
        return None

    auth_url = f"{API_BASE_URL}?{urlencode({'email': EMAIL, 'password': PASSWORD})}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(auth_url) as response:
                response.raise_for_status()
                token_data = await response.json()
                return token_data.get("token")

        except aiohttp.ClientError as e:
            print(f"❌ Authentication error: {e}")
            return None

async def fetch_players(session, token, offset, all_tr_ids, semaphore):
    """Fetch players asynchronously and count unique TR_IDs."""
    base_url = "https://apiprod.transferroom.com/api/external/players"
    headers = {"Authorization": f"Bearer {token}"}

    async with semaphore:
        request_url = f"{base_url}?offset={offset}&limit={LIMIT_PER_REQUEST}"
        
        try:
            async with session.get(request_url, headers=headers) as response:
                if response.status == 429:  # Rate limit exceeded
                    print("⏳ Rate limit hit! Sleeping for 60 seconds...")
                    await asyncio.sleep(RATE_LIMIT_SLEEP)
                    return await fetch_players(session, token, offset, all_tr_ids, semaphore)

                response.raise_for_status()
                players_data = await response.json()

                if not players_data:
                    return  # Stop fetching if no more players are returned

                for player in players_data:
                    tr_id = player.get("TR_ID")
                    if tr_id:
                        all_tr_ids.add(tr_id)  # Add unique TR_ID

        except aiohttp.ClientError as e:
            print(f"❌ Error fetching players at offset {offset}: {e}")

async def count_unique_tr_ids(token):
    """Fetch all players and count unique TR_IDs."""
    all_tr_ids = set()  # Use a set to store unique TR_IDs
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    async with aiohttp.ClientSession() as session:
        offsets = range(0, 200000, LIMIT_PER_REQUEST)  # Fetch up to 200,000 players
        tasks = [fetch_players(session, token, offset, all_tr_ids, semaphore) for offset in offsets]

        await asyncio.gather(*tasks)

    return len(all_tr_ids)  # Return total unique TR_ID count

async def main():
    """Main function to authenticate and count TR_IDs."""
    print("🚀 Starting TR_ID count...")
    start_time = time.time()

    token = await fetch_api_token()
    if not token:
        print("❌ Unable to fetch API token. Exiting...")
        return

    unique_tr_id_count = await count_unique_tr_ids(token)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"✅ Total Unique TR_IDs: {unique_tr_id_count}")
    print(f"⏳ Time Taken: {elapsed_time:.2f} seconds")

# Run the asyncio event loop
if __name__ == "__main__":
    asyncio.run(main())
