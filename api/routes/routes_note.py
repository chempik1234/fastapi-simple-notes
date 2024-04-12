from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from api.deps import CurrentUser, get_db
from schema.note_schema import SchemaNote, SchemaNoteList, SchemaNoteDB, SchemaNoteOptional
from crud import crud_note

router = APIRouter()


@router.get("/notes/", response_model=SchemaNoteList)
async def get_notes(user_id: Optional[int], db= Depends(get_db)) -> SchemaNoteList:
    notes = await crud_note.get_note_list(db, user_id)
    return SchemaNoteList(notes=notes)


@router.get("/notes/{note_id}", response_model=SchemaNote)
async def get_note(note_id: int, db= Depends(get_db)):
    note = await crud_note.get_note(db, note_id)
    if note:
        return note
    else:
        raise HTTPException(404, f"Не найдена запись Note с id={note_id}")


@router.post('/notes/', response_model=SchemaNoteDB)
async def create_note(note: SchemaNote, current_user: CurrentUser, db= Depends(get_db)):
    created_note = await crud_note.create_note(db, note, current_user)
    return created_note


@router.put('/notes/{note_id}', response_model=SchemaNote)
async def change_note(note_id: int, note: SchemaNoteOptional, db= Depends(get_db)):
    changed_note = await crud_note.change_note(db, note_id, note)
    if not changed_note:
        raise HTTPException(404, f"Не найдена запись Note с id={note_id}")
    return changed_note


@router.delete('/notes/{note_id}')
async def delete_note(note_id: int, db= Depends(get_db)):
    await crud_note.delete_note(db, note_id)
