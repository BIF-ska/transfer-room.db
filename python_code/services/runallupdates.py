import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
import subprocess
import sys
from agencyinsert import seed_agency
from competitioninsert import seed_competitions
from playerinsert import seed_players
from countryinsert import seed_countries
from playerAgencyinsert import seed_player_agencies
from Playermetricsinsert import seed_player_metrics
from teamsInsert import seed_teams




def main():
    """Runs all update scripts in sequence."""
    print("🚀 Starting database updates...")

    # ✅ Call each function directly instead of using subprocess
    try:
        print("🏢 Seeding Agencies...")
        seed_agency()
        print("✅ Agencies Updated!\n")

        print("🏆 Seeding Competitions...")
        seed_competitions()
        print("✅ Competitions Updated!\n")

        print("⚽ Seeding Players...")
        seed_players()
        print("✅ Players Updated!\n")

        print("🌍 Seeding Countries...")
        seed_countries()
        print("✅ Countries Updated!\n")

        print("🤝 Seeding Player Agencies...")
        seed_player_agencies()
        print("✅ Player Agencies Updated!\n")

        print("📊 Seeding Player Metrics...")
        seed_player_metrics()
        print("✅ Player Metrics Updated!\n")

        print("🏟️ Seeding Teams...")
        seed_teams()
        print("✅ Teams Updated!\n")

        print("🎉 All updates completed successfully!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()