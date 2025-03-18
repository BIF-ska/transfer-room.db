from apscheduler.schedulers.blocking import BlockingScheduler
import sys
from pathlib import Path
from datetime import datetime

# Ensure correct import paths
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))

# Import function from runallupdates.py
from services.runallupdates import run_all_updates

# Initialize the scheduler
scheduler = BlockingScheduler()

@scheduler.scheduled_job("cron", hour=0)  # Runs daily at midnight UTC
def scheduled_task():
    print(f"🚀 Running scheduled update at {datetime.utcnow()} UTC")
    run_all_updates()  # ✅ Corrected function call
    print("✅ Scheduled update completed!")

if __name__ == "__main__":
    print("📅 Scheduler started. Running updates now...")
    run_all_updates()  # ✅ Run immediately at startup
    scheduler.print_jobs()  # ✅ Debugging: Print all scheduled jobs
    scheduler.start()
