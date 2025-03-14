import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))

from apscheduler.schedulers.blocking import BlockingScheduler
from python_code.services.runallupdates import run_all_updates

scheduler = BlockingScheduler()

@scheduler.scheduled_job("cron", hour=0)  # ✅ Runs daily at midnight UTC   
def scheduled_task():
    print("🚀 Running scheduled update...")
    run_all_updates
    print("✅ Scheduled update completed!")

if __name__ == "__main__":
    print("📅 Scheduler started. Waiting for the next run...")
    scheduler.start()
