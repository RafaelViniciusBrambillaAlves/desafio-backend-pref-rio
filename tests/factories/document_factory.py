from app.models.document import Document
from bson import ObjectId
from datetime import datetime, UTC

def make_document(user_id: ObjectId | None = None) -> Document:
    user_id = user_id or ObjectId()

    return Document(
        id = ObjectId(),
        user_id = user_id,
        object_name = f"documents/{user_id}/file.png",
        content_type = "image/png",
        created_at = datetime.now(UTC)
    )

