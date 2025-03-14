from apscheduler.schedulers.blocking import BlockingScheduler
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))
from services.runallupdates import main
scheduler = BlockingScheduler()

@scheduler.scheduled_job("cron", hour=0)  # Runs every day at midnight (UTC)
def scheduled_task():
    print("🚀 Running scheduled update...")
    main()  # ✅ This will execute `run_all_updates.py`
    print("✅ Scheduled update completed!")

if __name__ == "__main__":
    print("🔄 Scheduler started, waiting for next execution...")
    scheduler.start()
