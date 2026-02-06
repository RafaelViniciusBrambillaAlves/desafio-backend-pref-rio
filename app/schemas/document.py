from pydantic import BaseModel 

class DocumentItem(BaseModel):
    path: str

class DocumentListResponse(BaseModel):
    documents: list[DocumentItem]

class DocumentUploadResponse(BaseModel):
    path: str