from typing import Optional
from fastapi import APIRouter, HTTPException

from api.deps import CurrentUser, DBSession
from schema.note_schema import SchemaNoteBasic, SchemaNoteList, SchemaNoteDB, SchemaNoteOptional, SchemaNoteWithId, \
    SchemaNoteWithUserId, SchemaNoteAmount
from crud import crud_note

router = APIRouter()


@router.get("/notes/amount/{user_id}", response_model=SchemaNoteAmount)
async def get_notes_amount(db: DBSession, user_id: int) -> SchemaNoteAmount:
    notes = await crud_note.get_note_amount(db, user_id)
    return SchemaNoteAmount(amount=notes)


@router.get("/notes/", response_model=SchemaNoteList)
async def get_notes(db: DBSession, user_id: Optional[int]) -> SchemaNoteList:
    notes = await crud_note.get_note_list(db, user_id)
    valid_notes = [SchemaNoteWithUserId(title=i.title, content=i.content, id=i.id, user_id=i.user_id) for i in notes]
    return SchemaNoteList(notes=valid_notes)


@router.get("/notes/{note_id}", response_model=SchemaNoteWithUserId)
async def get_note(db: DBSession, note_id: int):
    note = await crud_note.get_note(db, note_id)
    if note:
        return note
    else:
        raise HTTPException(404, f"Не найдена запись Note с id={note_id}")


@router.post('/notes/', response_model=SchemaNoteDB)
async def create_note(db: DBSession, note: SchemaNoteBasic, current_user: CurrentUser):
    created_note = await crud_note.create_note(db, note, current_user)
    return created_note


@router.put('/notes/{note_id}', response_model=SchemaNoteWithUserId)
async def change_note(db: DBSession, note_id: int, note: SchemaNoteOptional):
    changed_note = await crud_note.change_note(db, note_id, note)
    if not changed_note:
        raise HTTPException(404, f"Не найдена запись Note с id={note_id}")
    return changed_note


@router.delete('/notes/{note_id}')
async def delete_note(db: DBSession, note_id: int):
    await crud_note.delete_note(db, note_id)
