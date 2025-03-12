import sys 
import asyncio
from pathlib import Path
# Ensure the script can find parent modules
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from sqlalchemy.exc import SQLAlchemyError
from util.apiclient import APIClient
from models.players import Players
from models.playerMetrics import playerMetrics
from util.database import Database
from dotenv import load_dotenv
from datetime import datetime



import asyncio
import json

class PlayerMetricsFetcher:
    """Class to fetch and print player metrics for competition_id 487."""

    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    async def fetch_and_print_metrics(self):
        """Fetch player metrics for competition 487 and print the response."""
        
        print("📡 Fetching players for competition ID 487...")
        players_data = await self.api_client.fetch_players_487()

        print(f"✅ {len(players_data)} players retrieved from competition 487.\n")

        # ✅ Print full API response in JSON format
        print("🔍 FULL API RESPONSE:\n")
        print(json.dumps(players_data, indent=4))  # Pretty print JSON response

        # ✅ Print only the first 5 players separately for readability
        print("\n🔍 FIRST 5 PLAYERS PREVIEW:\n")
        print(json.dumps(players_data[:5], indent=4))  # Show only first 5 players

# ✅ Run the fetcher
if __name__ == "__main__":
    api_client = APIClient()
    fetcher = PlayerMetricsFetcher(api_client)

    # Run the process asynchronously
    asyncio.run(fetcher.fetch_and_print_metrics())
