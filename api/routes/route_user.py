from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from api.deps import CurrentUser, DBSession
from schema.user_schema import SchemaUser, SchemaUserOptional, SchemaUserDb, SchemaUserWithToken, \
    SchemaUserWithPassword, SchemaUserLogin, StupidOpenApiSchemaLogin
from crud import crud_user
from utils.utils_jwt import create_access_token, create_refresh_token
from utils.password_utils import verify_password

router = APIRouter()


@router.get('/users/{user_id}', response_model=SchemaUser)
async def get_user_by_id(db: DBSession, user_id: int) -> SchemaUser:
    user = await crud_user.get_user_by_id(db, user_id)
    if user:
        return user
    else:
        raise HTTPException(404, f"Не найден пользователь с id={user_id}")


@router.get('/users/by-login/{login}', response_model=SchemaUser)
async def get_user_by_login(db: DBSession, login: str) -> SchemaUser:
    user = await crud_user.get_user_by_login(db, login)
    if user:
        return user
    else:
        raise HTTPException(404, f"Не найден пользователь с login={login}")


@router.post('/users/', response_model=SchemaUserDb)
async def create_user(db: DBSession, user: SchemaUserWithPassword):
    existing_user = await crud_user.get_user_by_login(db, user.login)
    if existing_user:
        raise HTTPException(400, "Пользователь с таким login уже есть.")
    created_user = await crud_user.create_user(db, user)
    if created_user:
        return created_user
    else:
        raise HTTPException(500, "Пользователь не создан.")


@router.put('/users/{user_id}', response_model=SchemaUserDb)
async def put_user(db: DBSession, user_id: int, user: SchemaUserOptional):
    changed_user = await crud_user.change_user(db, user_id=user_id, user=user)
    if changed_user:
        return changed_user
    else:
        raise HTTPException(404, f"Пользователь с id={user_id} не найден.")


@router.delete('/users/{user_id}')
async def delete_user(db: DBSession, user_id: int):
    await crud_user.delete_user(db, user_id)


@router.post("/sign-up", response_model=SchemaUserWithToken)
async def user_sign_up(db: DBSession, user: SchemaUserWithPassword) -> SchemaUser:
    existing_user = await crud_user.get_user_by_login(db, user.login)
    if existing_user:
        raise HTTPException(400, "Пользователь с таким login уже есть.")
    created_user = await crud_user.create_user(db, user)
    if created_user:
        return SchemaUserWithToken(login=created_user.login,
                                   password=created_user.password,
                                   id=created_user.id,
                                   token=create_access_token(user))
    else:
        raise HTTPException(500, "Пользователь не создан.")


@router.post("/token/", response_model=StupidOpenApiSchemaLogin)
async def user_token(db: DBSession, response: Response, form_data: OAuth2PasswordRequestForm = Depends()) -> (
        StupidOpenApiSchemaLogin):
    existing_user = await crud_user.get_user_by_login(db, form_data.username)
    if not existing_user:
        raise HTTPException(404, "Пользователь с таким login не существует.")
    if verify_password(form_data.password, existing_user.password):
        token = create_refresh_token(existing_user)
        response.set_cookie(key="Authorization", value=token)
        return StupidOpenApiSchemaLogin(  # login=existing_user.login,
                                        # password=existing_user.password,
                                        # id=existing_user.id,
                                        # token=token,
                                        access_token=token,
                                        token_type="bearer")
    else:
        raise HTTPException(400, "Неверный пароль.")


@router.get("/users/me/", response_model=SchemaUser)
async def me(current_user: CurrentUser):
    return current_user

