import pytest
from bson import ObjectId
from unittest.mock import AsyncMock
from app.application.use_cases.document.list_user_documents_use_case import ListUserDocumentsUseCase
from datetime import datetime, UTC
from app.models.document import Document
from tests.factories.document_factory import make_document

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "documents_count",
    [2, 0]
)
async def test_list_documents_success(documents_count):

    user_id = ObjectId()

    documents = [
        make_document(user_id) for _ in range(documents_count)
    ]

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None

    mock_uow.documents = AsyncMock()
    mock_uow.documents.list_by_user = AsyncMock(return_value = documents)

    use_case = ListUserDocumentsUseCase(mock_uow)

    result = await use_case.execute(user_id)

    mock_uow.documents.list_by_user.assert_awaited_once_with(user_id)
    
    assert result == documents
    assert len(result) == len(documents)