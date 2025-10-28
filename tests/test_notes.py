import pytest
from httpx import AsyncClient
from app.main import app
from app.core.security import get_password_hash, create_access_token
from app.db.session import db
from bson import ObjectId


@pytest.mark.asyncio
async def test_notes_crud_and_rbac():
    # Cleanup
    await db.organizations.delete_many({})
    await db.users.delete_many({})
    await db.notes.delete_many({})

    # Create org
    org_result = await db.organizations.insert_one({"name": "NotesTestOrg"})
    org_id = str(org_result.inserted_id)

    # Helper: create user and return token
    async def create_user_and_token(email: str, role: str) -> str:
        await db.users.insert_one({
            "email": email,
            "hashed_password": get_password_hash("password123"),
            "role": role,
            "org_id": ObjectId(org_id)
        })
        # Login to get token
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.post(
                f"/api/v1/organizations/{org_id}/users/login",
                json={"email": email, "password": "password123"}
            )
            return response.json()["access_token"]

    reader_token = await create_user_and_token("reader@example.com", "reader")
    writer_token = await create_user_and_token("writer@example.com", "writer")
    admin_token = await create_user_and_token("admin@example.com", "admin")

    async with AsyncClient(app=app, base_url="http://test") as ac:
        # ✅ Writer creates note
        response = await ac.post(
            "/api/v1/notes/",
            json={"title": "Test Note", "content": "Hello"},
            headers={"Authorization": f"Bearer {writer_token}"}
        )
        assert response.status_code == 200
        note_id = response.json()["id"]

        # ❌ Reader cannot create note
        response = await ac.post(
            "/api/v1/notes/",
            json={"title": "Forbidden", "content": "Nope"},
            headers={"Authorization": f"Bearer {reader_token}"}
        )
        assert response.status_code == 403

        # ✅ All roles can list and read notes
        for token in [reader_token, writer_token, admin_token]:
            response = await ac.get("/api/v1/notes/", headers={"Authorization": f"Bearer {token}"})
            assert response.status_code == 200
            assert len(response.json()) == 1

            response = await ac.get(f"/api/v1/notes/{note_id}", headers={"Authorization": f"Bearer {token}"})
            assert response.status_code == 200

        # ✅ Admin deletes note
        response = await ac.delete(
            f"/api/v1/notes/{note_id}",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200

        # ❌ Note is gone for all users
        for token in [reader_token, writer_token]:
            response = await ac.get(f"/api/v1/notes/{note_id}", headers={"Authorization": f"Bearer {token}"})
            assert response.status_code == 404




