from pydantic import BaseModel,  Field
from app.models.common import PyObjectId

class NoteModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    org_id: PyObjectId
    owner_id: PyObjectId

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True