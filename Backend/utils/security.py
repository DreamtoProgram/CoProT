from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

from Backend.config import (
    JWT_SECRET,
    JWT_ALGORITHM,
    JWT_EXPIRATION_MINUTES
)


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: int) -> str:

    expiration = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_EXPIRATION_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expiration
    }

    token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return token