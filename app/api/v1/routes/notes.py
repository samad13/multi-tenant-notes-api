from fastapi import APIRouter, Depends, HTTPException, Path, Body
from app.api.deps import require_role
from app.services.note_service import create_note, get_notes_by_org, get_note_by_id, delete_note

router = APIRouter()

@router.post("/", dependencies=[Depends(require_role("writer"))])
async def create_note_endpoint(
    current_user: dict = Depends(require_role("writer")),
    data: dict = Body(...)
):
    note = await create_note(
        title=data["title"],
        content=data["content"],
        org_id=current_user["org_id"],
        owner_id=current_user["id"]
    )
    return {"id": str(note.id), "title": note.title}

@router.get("/", dependencies=[Depends(require_role("reader"))])
async def list_notes(current_user: dict = Depends(require_role("reader"))):
    notes = await get_notes_by_org(current_user["org_id"])
    return [{"id": str(n["_id"]), "title": n["title"]} for n in notes]

@router.get("/{note_id}", dependencies=[Depends(require_role("reader"))])
async def get_note(
    note_id: str = Path(...),
    current_user: dict = Depends(require_role("reader"))
):
    note = await get_note_by_id(note_id, current_user["org_id"])
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return {
        "id": str(note["_id"]),
        "title": note["title"],
        "content": note["content"]
    }

@router.delete("/{note_id}", dependencies=[Depends(require_role("admin"))])
async def delete_note_endpoint(
    note_id: str = Path(...),
    current_user: dict = Depends(require_role("admin"))
):
    success = await delete_note(note_id, current_user["org_id"])
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"detail": "Note deleted"}