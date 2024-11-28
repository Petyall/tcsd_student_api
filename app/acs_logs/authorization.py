import os

from fastapi import HTTPException
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError

from app.config import settings


def generate_token():
    expiration = datetime.utcnow() + timedelta(days=settings.TOKEN_EXPIRY_DAYS)
    token = jwt.encode({"exp": expiration}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    with open(settings.TOKEN_STORAGE, "w") as f:
        f.write(token)
    return token


def verify_token(token: str) -> bool:
    if not os.path.exists(settings.TOKEN_STORAGE):
        generate_token()
    with open(settings.TOKEN_STORAGE, "r") as f:
        stored_token = f.read().strip()
    if token != stored_token:
        raise HTTPException(status_code=404, detail="Токен не существует")
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise HTTPException(status_code=404, detail="Токен просрочен")
    except JWTError:
        raise HTTPException(status_code=404, detail="Неверный формат токена")

    return True
