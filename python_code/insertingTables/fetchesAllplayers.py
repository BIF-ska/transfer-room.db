import os
import json
import asyncio
import aiohttp
from urllib.parse import urlencode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from aiohttp import ClientTimeout

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a database engine
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=False)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Maximum number of concurrent requests (adjust as needed)
MAX_CONCURRENT_REQUESTS = 5

# Timeout settings
REQUEST_TIMEOUT = ClientTimeout(total=30)  # Increase timeout to 30 seconds


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
            print(f"Error during authentication: {e}")
            return None


async def fetch_competitions(token):
    """Fetch all available competitions and remove duplicates."""
    request_url = "https://apiprod.transferroom.com/api/external/competitions"
    headers = {"Authorization": f"Bearer {token}"}

    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
        try:
            async with session.get(request_url, headers=headers) as response:
                response.raise_for_status()
                json_data = await response.json()

                # Extract unique competition IDs
                seen_ids = set()
                unique_competitions = []
                
                for comp in json_data:
                    comp_id = comp.get("id")
                    if comp_id and comp_id not in seen_ids:
                        seen_ids.add(comp_id)
                        unique_competitions.append(comp)

                print(f"Total Unique Competitions Found: {len(unique_competitions)}")
                return unique_competitions

        except aiohttp.ClientError as e:
            print(f"Error fetching competitions: {e}")
            return []




    offset = 0  # Start from the first player

    async with semaphore:  # Limit the number of simultaneous requests
        while True:
            request_url = f"https://apiprod.transferroom.com/api/external/players?position=0&amount=1000&competitionid={competition_id}&offset={offset}"
            headers = {"Authorization": f"Bearer {token}"}

            try:
                async with session.get(request_url, headers=headers, timeout=REQUEST_TIMEOUT) as response:
                    response.raise_for_status()
                    json_data = await response.json()

                    players = json_data if isinstance(json_data, list) else json_data.get("players", [])

                    if not players:
                        break  # No more players to fetch

                    all_players.extend(players)
                    offset += len(players)  # Increase offset to get the next batch
                    print(f"Fetched {len(players)} players from competition {competition_id}, total so far: {len(all_players)}")

            except asyncio.TimeoutError:
                print(f"Timeout fetching players for competition {competition_id}. Retrying...")
                await asyncio.sleep(2)  # Wait and retry
            except aiohttp.ClientError as e:
                print(f"Error fetching players for competition {competition_id}: {e}")
                break  # Stop fetching if there's an error

    return all_players


    """Fetch ALL player data for a given competition asynchronously, using pagination."""
    all_players = []
    offset = 0  # Start from the first player

    async with semaphore:  # Limit the number of simultaneous requests
        while True:
            request_url = f"https://apiprod.transferroom.com/api/external/players?position=0&amount=1000&competitionid={competition_id}&offset={offset}"
            headers = {"Authorization": f"Bearer {token}"}

            try:
                async with session.get(request_url, headers=headers, timeout=REQUEST_TIMEOUT) as response:
                    response.raise_for_status()
                    json_data = await response.json()

                    players = json_data if isinstance(json_data, list) else json_data.get("players", [])

                    if not players:  # 🛑 STOP when there are no more players to fetch
                        print(f"Finished fetching players for competition {competition_id}. Total: {len(all_players)}")
                        break  

                    all_players.extend(players)
                    offset += len(players)  # Increase offset to get the next batch
                    print(f"Fetched {len(players)} players from competition {competition_id}, total so far: {len(all_players)}")

            except asyncio.TimeoutError:
                print(f"Timeout fetching players for competition {competition_id}. Retrying...")
                await asyncio.sleep(2)  # Wait and retry
            except aiohttp.ClientError as e:
                print(f"Error fetching players for competition {competition_id}: {e}")
                break  # Stop fetching if there's an error

    return all_players


async def fetch_players_by_competition(session, token, competition_id, semaphore):
    """Fetch ALL player data for a given competition asynchronously, using pagination."""
    all_players = []
    offset = 0  # Start from the first player
    last_batch_size = -1  # Tracks last batch size to detect infinite loops

    async with semaphore:  # Limit the number of simultaneous requests
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
                        break  # 🛑 Stop fetching when no more players

                    all_players.extend(players)
                    offset += len(players)  # Increase offset to get the next batch

                    # 🛑 Stop if we keep getting the same number of players (API issue)
                    if last_batch_size == len(players):
                        print(f"⚠️ Pagination loop detected in competition {competition_id}. Stopping to avoid infinite loop.")
                        break

                    last_batch_size = len(players)  # Update last batch size
                    print(f"Fetched {len(players)} players from competition {competition_id}, total so far: {len(all_players)}")

            except asyncio.TimeoutError:
                print(f"⏳ Timeout fetching players for competition {competition_id}. Retrying...")
                await asyncio.sleep(2)  # Wait and retry
            except aiohttp.ClientError as e:
                print(f"❌ Error fetching players for competition {competition_id}: {e}")
                break  # Stop fetching if there's an error

    return all_players


async def fetch_all_players():
    """Fetch all players from all competitions asynchronously with limited concurrency."""
    token = await fetch_api_token()
    if not token:
        print("Failed to authenticate.")
        return

    competitions = await fetch_competitions(token)
    all_players = []

    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)  # Limit concurrency
    async with aiohttp.ClientSession(timeout=REQUEST_TIMEOUT) as session:
        tasks = []
        for competition in competitions:
            competition_id = competition.get("id")  # Use 'id' instead of 'competitionid'
            if competition_id:
                tasks.append(fetch_players_by_competition(session, token, competition_id, semaphore))

        # Run limited requests in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Flatten results into all_players list
        for result in results:
            if isinstance(result, list):
                all_players.extend(result)

    print(f"Grand Total Players Fetched: {len(all_players)}")
    
    # Save results to a file
    with open("players_data.json", "w") as f:
        json.dump(all_players, f, indent=4)

    print("Player data saved to players_data.json")
    return all_players


if __name__ == "__main__":
    asyncio.run(fetch_all_players())
