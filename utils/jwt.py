import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt


ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    return create_token(subject, JWT_SECRET_KEY, expires_delta, ACCESS_TOKEN_EXPIRE_MINUTES)


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    return create_token(subject, JWT_SECRET_KEY, expires_delta, REFRESH_TOKEN_EXPIRE_MINUTES)


def create_token(subject: Union[str, Any], secret: str, expires_delta, default_delta_minutes) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=default_delta_minutes)

    token_data = {"exp": expires_delta, "sub": str(subject)}
    encoded = jwt.encode(token_data, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded
