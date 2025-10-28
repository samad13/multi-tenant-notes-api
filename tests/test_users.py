import pytest
from httpx import AsyncClient
from app.main import app
from app.core.security import get_password_hash
from app.db.session import db
from bson import ObjectId


@pytest.mark.asyncio
async def test_user_registration_and_login():
    # Cleanup
    
    await db.organizations.delete_many({})
    await db.users.delete_many({})

    # Create org
    org_result = await db.organizations.insert_one({"name": "LoginTestOrg"})
    org_id = str(org_result.inserted_id)
    fake_org_id = "000000000000000000000000"

    email = "user@example.com"
    password = "password123"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # === Registration ===
        response = await ac.post(
            f"/api/v1/organizations/{org_id}/users/",
            json={"email": email, "password": password, "role": "writer"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

        # === Login: Valid credentials ===
        response = await ac.post(
            f"/api/v1/organizations/{org_id}/users/login",
            json={"email": email, "password": password}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()

        # === Login: Invalid password ===
        response = await ac.post(
            f"/api/v1/organizations/{org_id}/users/login",
            json={"email": email, "password": "wrongpass"}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"

        # === Login: Non-existent email ===
        response = await ac.post(
            f"/api/v1/organizations/{org_id}/users/login",
            json={"email": "fake@example.com", "password": password}
        )
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid email or password"

        # === Login: Invalid org_id ===
        response = await ac.post(
            f"/api/v1/organizations/{fake_org_id}/users/login",
            json={"email": email, "password": password}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Organization not found"