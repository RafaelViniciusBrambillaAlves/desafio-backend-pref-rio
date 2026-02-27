import pytest
from bson import ObjectId
from app.models.user import User
from unittest.mock import AsyncMock
from app.main import app
from app.core.auth_dependencies import get_current_user
from app.dependencies.document_dependencies import get_list_user_documents_use_case
from httpx import ASGITransport, AsyncClient
from fastapi import status
from tests.factories.document_factory import make_document
from app.application.use_cases.document.list_user_documents_use_case import ListUserDocumentsUseCase

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "documents_count",
    [0, 2]
)
async def test_list_my_document_sucess(documents_count: int):

    user_id = ObjectId()

    fake_user = User(
        id = user_id,
        email = "test@test.com"
    )

    documents = [make_document(user_id = user_id) for _ in range(documents_count)]

    mock_use_case = AsyncMock(spec = ListUserDocumentsUseCase)
    mock_use_case.execute = AsyncMock(return_value = documents)

    async def override_get_current_user():
        return fake_user
    
    async def override_get_use_case():
        return mock_use_case
    
    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[get_list_user_documents_use_case] = override_get_use_case

    transport = ASGITransport(app = app)

    async with AsyncClient(
        transport = transport,
        base_url = "http://test"
    ) as client:
        response = await client.get(
            "/users/me/documents"
        )

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["message"] == "Documents listed successfully."
    assert "data" in body
    assert "documents" in body["data"]

    returned_documents = body["data"]["documents"]

    assert len(returned_documents) == documents_count

    if documents_count > 0:
        assert returned_documents[0]["path"] == documents[0].object_name

    mock_use_case.execute.assert_awaited_once_with(user_id = user_id)

    app.dependency_overrides.clear()

