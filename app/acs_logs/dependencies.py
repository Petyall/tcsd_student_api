from app.acs_logs.authorization import TokenManager
from app.config import settings


token_manager = TokenManager(
    secret_key=settings.SECRET_KEY,
    algorithm=settings.ALGORITHM,
    token_expiry_days=settings.TOKEN_EXPIRY_DAYS,
    token_storage=settings.TOKEN_STORAGE,
)
