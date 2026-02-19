from jose import jwt
from app.core.config import settings
from datetime import datetime, timedelta, timezone
import uuid
import datetime

class JWTService:  
    ISSUER = "transport-api"

    @staticmethod
    def create_access_token(user_id: int) -> str:
        # now = datetime.now(timezone.utc)
        now = datetime.datetime.now(datetime.timezone.utc)

        payload = {
            "sub": str(user_id),
            "type": "access",
            "iss": JWTService.ISSUER,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes = settings.JWT_REFRESH_TOKEN_EXPIRES_MINUTES)).timestamp()),
            "jti": str(uuid.uuid4)
        }       

        return jwt.encode(
            payload, 
            settings.JWT_SECRET_KEY, 
            algorithm = settings.JWT_ALGORITHM
            )

    @staticmethod
    def create_refresh_token(user_id: int) -> str:
        # now = datetime.now(timedelta.utc)
        now = datetime.datetime.now(datetime.timezone.utc)

        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "iss": JWTService.ISSUER,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(days = settings.JWT_REFRESH_TOKEN_EXPIRES_DAYS)).timestamp())
        } 

        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm = settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str):
        return jwt.decode(
            token, 
            settings.JWT_SECRET_KEY,
            algorithms = [settings.JWT_ALGORITHM],
            issuer = JWTService.ISSUER
        )