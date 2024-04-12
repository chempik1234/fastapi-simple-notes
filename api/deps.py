from typing import Annotated

from fastapi import Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession, async_session
from sqlalchemy.orm import Session

from db.session import SessionLocal, create_session
from models.models import User
from crud.crud_user import get_user_by_token
from utils.utils_jwt import oauth2_scheme


# async def get_db() -> AsyncSession:
#     async with SessionLocal() as session:
#         yield session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """Get user based on token."""
    user = await get_user_by_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


DBSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
