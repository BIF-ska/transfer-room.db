from apscheduler.schedulers.blocking import BlockingScheduler
import sys
from pathlib import Path
from datetime import datetime
import logging


# Ensure correct import paths
sys.path.append(str(Path(__file__).parents[1]))
sys.path.append(str(Path(__file__).parents[0]))

# Import function from runallupdates.py
from services.runallupdates import run_all_updates

scheduler = BlockingScheduler()

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger()

@scheduler.scheduled_job("cron", hour=0)  # Runs daily at midnight UTC
def scheduled_task():
    logger.info(f"🚀 Running scheduled update at {datetime.utcnow()} UTC")
    try:
        run_all_updates()
        logger.info("✅ Scheduled update completed!")
    except Exception as e:
        logger.error(f"❌ An error occurred during scheduled update: {e}")

# Run the task immediately when the script starts
if __name__ == "__main__":
    scheduled_task()  # Trigger now
    scheduler.start()  # Continue running as scheduled