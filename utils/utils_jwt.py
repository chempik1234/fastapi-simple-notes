import os
from datetime import datetime, timedelta
from typing import Union, Any

from fastapi import Depends
from jose import jwt

from core.config import settings
from fastapi.security import OAuth2PasswordBearer

from models.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30
ALGORITHM = "HS256"
JWT_SECRET_KEY = settings.JWT_SECRET_KEY  # os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = settings.JWT_REFRESH_SECRET_KEY  # os.environ['JWT_REFRESH_SECRET_KEY']


def create_access_token(subject: User) -> str:
    return create_token(subject, JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES)


def create_refresh_token(subject: User) -> str:
    return create_token(subject, JWT_SECRET_KEY, REFRESH_TOKEN_EXPIRE_MINUTES)


def create_token(subject: User, secret: str, expires_delta) -> str:
    expires_delta = datetime.utcnow() + timedelta(minutes=expires_delta)
    token_data = {"exp": expires_delta, "sub": subject.login, "audience": "Authenticated"}
    print(token_data)
    encoded = jwt.encode(token_data, secret, algorithm=ALGORITHM)
    return encoded


def decode_token(token: str = Depends(oauth2_scheme)):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
