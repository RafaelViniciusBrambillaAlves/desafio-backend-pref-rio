import pytest
from bson import ObjectId
from app.models.user import User
from unittest.mock import AsyncMock
from app.application.use_cases.document.upload_document_use_case import UploadDocumentUseCase
from app.main import app
from app.core.auth_dependencies import get_current_user
from app.dependencies.document_dependencies import get_upload_document_use_case
from httpx import ASGITransport, AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_upload_cnh_photo_route_success(client):

    user_id = ObjectId()

    fake_user = User(
        id = user_id,
        email = "test@test.com"
    )

    mock_use_case = AsyncMock(spec = UploadDocumentUseCase)
    mock_use_case.execute = AsyncMock(return_value = "documents/test/file.png")

    async def override_get_current_user():
        return fake_user
    
    async def override_get_use_case():
        return mock_use_case
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_upload_document_use_case] = override_get_use_case

    try:
        response = await client.post(
            "/users/me/cnh-photo",
            files = {"file": ("file.png", b"fake-image", "image/png")}
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["message"] == "Document upload successfuly."
        assert response.json()["data"]["path"] == "documents/test/file.png"

        mock_use_case.execute.assert_awaited_once()

    finally:

        app.dependency_overrides.clear()