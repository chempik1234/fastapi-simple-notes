from typing import Optional

from pydantic import BaseModel


class SchemaNote(BaseModel):
    title: str
    content: str


class SchemaNoteUserId(SchemaNote):
    user_id: int


class SchemaNoteList(BaseModel):
    notes: list[SchemaNote]


class SchemaNoteDB(SchemaNoteUserId):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class SchemaNoteOptional(BaseModel):
    title: Optional[str]
    content: Optional[str]
    user_id: Optional[int]
