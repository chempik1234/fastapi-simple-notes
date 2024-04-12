from typing import Optional

from pydantic import BaseModel


class SchemaNote(BaseModel):
    id: int
    user_id: int
    title: str
    content: str


class SchemaNoteUserId(SchemaNote):
    pass


class SchemaNoteList(BaseModel):
    notes: list[SchemaNote]


class SchemaNoteDB(SchemaNoteUserId):
    # id: Optional[int] = None

    class Config:
        orm_mode = True


class SchemaNoteOptional(BaseModel):
    title: Optional[str]
    content: Optional[str]
    user_id: Optional[int]
