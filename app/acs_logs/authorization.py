import os

from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError

from app.logger import logger


class TokenManager:
    """Класс для работы с JWT-токенами

    Атрибуты
    ----------
    secret_key : str
        секретный ключ для алгоритма шифрования
    algorithm : str
        алгоритм шифрования
    token_expiry_days : int
        количество дней действия JWT-токена
    token_storage : str
        путь расположения файла с JWT-токеном

    Методы
    -------
    generate_token()
        Генерирует и сохраняет JWT-токен
    verify_token()
        Проводит верификацию предоставленного JWT-токена
    """

    def __init__(self, secret_key: str, algorithm: str, token_expiry_days: int, token_storage: str):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry_days = token_expiry_days
        self.token_storage = token_storage

    def generate_token(self) -> str:
        """Генерация и сохранение JWT-токена"""
        expiration = datetime.utcnow() + timedelta(days=self.token_expiry_days)
        token = jwt.encode({"exp": expiration}, self.secret_key, algorithm=self.algorithm)
        self._store_token(token)
        return token

    def verify_token(self, token: str) -> bool:
        """Верификация предоставленного JWT-токена"""
        stored_token = self._read_stored_token()
        if token != stored_token:
            logger.warning("Токен не совпадает с сохранённым")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Токен не существует")
        try:
            jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except ExpiredSignatureError:
            logger.warning("Просроченный токен")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен просрочен")
        except JWTError:
            logger.error("Ошибка декодирования токена")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный формат токена")

        return True

    def _store_token(self, token: str):
        """Сохранение файла с JWT-токеном"""
        with open(self.token_storage, "w") as f:
            f.write(token)

    def _read_stored_token(self) -> str:
        """Поиск и чтение файла с JWT-токеном"""
        if not os.path.exists(self.token_storage):
            return self.generate_token()
        with open(self.token_storage, "r") as f:
            return f.read().strip()
