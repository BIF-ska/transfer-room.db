from apscheduler.schedulers.blocking import BlockingScheduler
from your_script import main

scheduler = BlockingScheduler()

@scheduler.scheduled_job("cron", hour=0)  # Runs daily at midnight
def scheduled_task():
    print("Running scheduled update...")
    main()
    print("Scheduled update completed!")

if __name__ == "__main__":
    scheduler.start()
