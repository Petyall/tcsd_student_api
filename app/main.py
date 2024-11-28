import subprocess

from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from app.acs_logs.authorization import generate_token
from app.acs_logs.router import router as acs_logs_router


def get_logs():
    try:
        result = subprocess.run(["get_logs.bat"], capture_output=True, text=True, check=True)
        print(f"Логи успешно обработаны: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка выполнения BAT-файла: {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")


scheduler = BackgroundScheduler(timezone="Europe/Moscow")
scheduler.add_job(get_logs, "cron", hour=5, minute=30, id='get_logs_job')
scheduler.add_job(generate_token, 'cron', day='last', hour=23, minute=59, id='generate_token_job')


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)

app.include_router(acs_logs_router)
