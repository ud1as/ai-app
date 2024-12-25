from typing import List, Optional
from pydantic import BaseModel

class FileChunk(BaseModel):
    content: str
    chunk_index: int
    chunk_total: int

class FilePreviewResponse(BaseModel):
    chunks: List[FileChunk]
    total_chunks: int

class FileProcessResponse(BaseModel):
    success: bool
    dataset_id: Optional[str] = None
    error: Optional[str] = None

class FileProcessRequest(BaseModel):
    tenant_id: str