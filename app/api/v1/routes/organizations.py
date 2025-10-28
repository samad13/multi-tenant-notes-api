from fastapi import APIRouter, Body
from app.schemas.organization import OrganizationCreate
from app.services.organization_service import create_organization

router = APIRouter()

@router.post("/", response_model=dict)
async def create_org_endpoint(org: OrganizationCreate = Body(...)):
    created = await create_organization(org.name)
    return {"id": str(created.id), "name": created.name}