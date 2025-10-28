import pytest
from httpx import AsyncClient
from app.main import app
from app.db.session import db


@pytest.mark.asyncio
async def test_create_organization():
    # Cleanup
    await db.organizations.delete_many({})

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/organizations/",
            json={"name": "TestOrg"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == "TestOrg"