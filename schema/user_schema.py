from typing import Optional

from pydantic import BaseModel


class SchemaUser(BaseModel):
    id: int
    login: str


class SchemaUserWithPassword(SchemaUser):
    password: str


class SchemaUserDb(SchemaUserWithPassword):
    # id: int

    class Config:
        orm_mode = True


class SchemaUserOptional(BaseModel):
    login: Optional[str]
    password: Optional[str]


class SchemaUserLogin(BaseModel):
    login: str
    password: str


class SchemaUserWithToken(SchemaUserDb):
    token: str


class StupidOpenApiSchemaLogin(BaseModel):
    access_token: str
    token_type: str
