from apscheduler.schedulers.background import BackgroundScheduler

from app.tasks import get_logs
from app.acs_logs.dependencies import token_manager


def scheduler_setup():
    scheduler = BackgroundScheduler(timezone="Europe/Moscow")
    scheduler.add_job(get_logs, "cron", hour=16, minute=33, id='get_logs_job')
    scheduler.add_job(token_manager.generate_token, "cron", day='last', hour=23, minute=59, id='generate_token_job')
    return scheduler
