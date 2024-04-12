from typing import Optional
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Note, User
from schema.note_schema import SchemaNote, SchemaNoteOptional


async def get_note_list(db, user_id: Optional[int]) -> list[Note]:
    """
    CRUD async GET that returns a list of Notes and uses the only optional criterion (user_id)
    :param db that executes the statement
    :param user_id: optional parameter that lets you get only one's notes if it's not None
    :return: list of found Notes
    """
    statement = select(Note)
    if user_id is not None:
        statement = statement.where(Note.user_id == user_id)
    db_result = await db.execute(statement)
    return db_result.scalars().all()


async def get_note(db, note_id: int) -> Optional[Note]:
    """
    CRUD async GET that returns the Note with given note_id
    :param db that executes the statement
    :param note_id: required parameter that identifies a Note
    :return: the found Note or None
    """
    statement = select(Note).where(Note.id == note_id)
    result = await db.execute(statement)
    return result.scalars().first()


async def create_note(db, note: SchemaNote, user: User) -> Note:
    """
    CRUD async POST that creates a Note with given data
    :param db that executes the statement
    :param note: Note schema that contains the data
    :param user: the linked User that is set as the author
    :return: created Note
    """
    db_note = Note(title=note.title, content=note.content, user_id=user.id)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note


async def change_note(db, note_id: int, note: SchemaNoteOptional) -> Note:
    """
    CRUD async PUT that changes a Note. Giving new data is optional
    :param db that executes the statement
    :param note_id: required parameter that identifies a Note
    :param note: Model schema that contains the data
    :return: the changed Note with full data but id
    """
    values = {}
    if note.title is not None:
        values["title"] = note.title
    if note.content is not None:
        values["content"] = note.content
    if note.user_id is not None:
        values["user_id"] = note.user_id
    statement = update(Note).where(Note.id == note_id).values(**values)
    put_result = await db.execute(statement)
    return put_result.scalars().first()


async def delete_note(db, note_id: int) -> None:
    """
    CRUD async DELETE that deletes a Note with given note_id
    :param db that executes the statement
    :param note_id: required parameter that identifies a Note
    :return: None
    """
    statement = delete(Note).where(Note.id == note_id)
    await db.execute(statement)
    await db.commit()
