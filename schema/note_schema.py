from typing import Optional

from pydantic import BaseModel


class SchemaNoteAmount(BaseModel):
    amount: int


class SchemaNoteBasic(BaseModel):
    title: str
    content: str


class SchemaNoteWithId(SchemaNoteBasic):
    id: int


class SchemaNoteWithUserId(SchemaNoteWithId):
    user_id: int


class SchemaNoteList(BaseModel):
    notes: list[SchemaNoteWithUserId]


class SchemaNoteDB(SchemaNoteWithUserId):
    # id: Optional[int] = None

    class Config:
        orm_mode = True


class SchemaNoteOptional(BaseModel):
    title: Optional[str]
    content: Optional[str]
    user_id: Optional[int]
