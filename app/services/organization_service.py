from app.db.session import db
from app.models.organization import OrganizationModel

async def create_organization(name: str):
    org = OrganizationModel(name=name)
    result = await db.organizations.insert_one(org.dict(by_alias=True))
    org.id = result.inserted_id
    return org