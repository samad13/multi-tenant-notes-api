from app.db.session import db
from app.models.note import NoteModel
from bson import ObjectId

async def create_note(title: str, content: str, org_id: str, owner_id: str):
    note = NoteModel(
        title=title,
        content=content,
        org_id=org_id,
        owner_id=owner_id
    )
    result = await db.notes.insert_one(note.dict(by_alias=True))
    note.id = result.inserted_id
    return note

async def get_notes_by_org(org_id: str):
    cursor = db.notes.find({"org_id": ObjectId(org_id)})
    notes = await cursor.to_list(length=100)
    return notes

async def get_note_by_id(note_id: str, org_id: str):
    note = await db.notes.find_one({
        "_id": ObjectId(note_id),
        "org_id": ObjectId(org_id)
    })
    return note

async def delete_note(note_id: str, org_id: str):
    result = await db.notes.delete_one({
        "_id": ObjectId(note_id),
        "org_id": ObjectId(org_id)
    })
    return result.deleted_count > 0