import os
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.logger import logger
from app.scheduler import scheduler_setup
from app.acs_logs.router import router as acs_logs_router
from app.acs_logs.dependencies import token_manager


scheduler = scheduler_setup()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists("./token.txt"):
        logger.warning("Не найден файл с JWT токеном, начинаю попытку генерации...")
        token_manager.generate_token()
        logger.info("Успешно сгенерирован новый файл с JWT токеном!")

    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
app.include_router(acs_logs_router)
