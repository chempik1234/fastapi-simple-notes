from typing import Optional

from pydantic import BaseModel


class SchemaUser(BaseModel):
    login: str
    password: str


class SchemaUserDb(SchemaUser):
    id: int

    class Config:
        orm_mode = True


class SchemaUserOptional(BaseModel):
    login: Optional[str]
    password: Optional[str]
