from typing import Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from utils.utils_jwt import create_access_token, create_refresh_token, decode_token

from models.models import User
from schema.user_schema import SchemaUser, SchemaUserOptional, SchemaUserWithPassword
from utils.password_utils import get_hashed_password


async def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    CRUD async GET that returns the user with given id
    :param db: Session that executes the statement
    :param user_id: a required parameter that identifies the user
    :return: found User object
    """
    statement = select(User).where(User.id == user_id)
    result = db.execute(statement)
    return result.scalars().first()


async def get_user_by_login(db: Session, login: str) -> Optional[User]:
    """
    CRUD async GET that returns the user with given id
    :param db: Session that executes the statement
    :param login: a required parameter that identifies the user
    :return: found User object
    """
    statement = select(User).where(User.login == login)
    result = db.execute(statement)
    return result.scalars().first()


async def create_user(db: Session, user: SchemaUserWithPassword) -> Optional[User]:
    """
    CRUD async POST that creates and returns the user
    :param db: Session that executes the statement
    :param user: schema that contains the data
    :return: created User object or None if there's already a user with the same login
    """
    if (await get_user_by_login(db, user.login)) is None:
        new_user = User(login=user.login, password=get_hashed_password(user.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


async def change_user(db: Session, user_id: int, user: SchemaUserOptional) -> Optional[User]:
    """
    CRUD async POST that creates and returns the user
    :param db: Session that executes the statement
    :param user_id: a required parameter that identifies the user
    :param user:  schema that contains the data (which is optional to give)
    :return: changed User object or None if not found
    """
    values = {}
    if user.login is not None:
        values["login"] = user.login
    if user.password is not None:
        values["password"] = user.password
    statement = update(User).where(User.id == user_id).values(**values)
    put_result = db.execute(statement)
    return put_result.scalars().first()


async def delete_user(db: Session, user_id: int) -> None:
    """
    CRUD async DELETE that deletes a User with given note_id
    :param db: Session that executes the statement
    :param user_id: required parameter that identifies a User
    :return: None
    """
    statement = delete(User).where(User.id == user_id)
    db.execute(statement)
    db.commit()


async def get_user_by_token(db: Session, token: str) -> Optional[User]:
    """
    Async function that uses a token to get current user
    :param db: Session that executes the statement
    :param token: a JWT that defines the searched user
    :return: found User or None if it couldn't be found
    """
    token_dict = decode_token(token)
    login = token_dict.get('sub')
    if login:
        return await get_user_by_login(db, login)
