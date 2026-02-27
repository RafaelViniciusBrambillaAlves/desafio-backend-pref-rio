import pytest
from bson import ObjectId
from unittest.mock import AsyncMock
from app.application.use_cases.document.upload_document_use_case import UploadDocumentUseCase
from app.core.exceptions import AppException
from fastapi import status

class FakeUpdateFile:
    def __init__(self, content_type: str):
        self.content_type = content_type

@pytest.mark.asyncio
async def test_upload_document_success():
    
    user_id = ObjectId()

    file = FakeUpdateFile("image/png")

    mock_uow = AsyncMock()
    mock_uow.__aenter__.return_value = mock_uow
    mock_uow.__aexit__.return_value = None
    mock_uow.documents.create = AsyncMock()

    mock_storage = AsyncMock()
    mock_storage.update = AsyncMock()

    use_case = UploadDocumentUseCase(mock_uow, mock_storage)

    object_name = await use_case.execute(user_id, file)

    mock_storage.upload.assert_awaited_once()
    mock_uow.documents.create.assert_awaited_once()

    assert object_name.startswith("documents/")
    assert str(user_id) in object_name

@pytest.mark.asyncio
async def test_upload_document_invalid_image_format():
    
    user_id = ObjectId()
    file = FakeUpdateFile("application/pdf")

    mock_uow = AsyncMock()
    mock_storage = AsyncMock()

    use_case = UploadDocumentUseCase(mock_uow, mock_storage)

    with pytest.raises(AppException) as exc:
        await use_case.execute(user_id, file)

    assert exc.value.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert exc.value.error == "INVALID_IMAGE_FORMAT"

    mock_storage.upload.assert_not_called()
    