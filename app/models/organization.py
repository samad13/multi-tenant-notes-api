from pydantic import BaseModel, Field
from app.models.common import PyObjectId

class OrganizationModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True