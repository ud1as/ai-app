from typing import List, Optional
from pydantic import BaseModel
from pydantic import BaseModel, Field
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
    
class DatasetResponse(BaseModel):
    id: str = Field(..., description="Unique identifier of the dataset.")
    tenant_id: str = Field(..., description="Unique identifier for the tenant.")
    created_by: Optional[str] = Field(None, description="ID of the user who created the dataset.")
    name: Optional[str] = Field(None, description="Name of the dataset.")
    
class DatasetRequest(BaseModel):
    name: str = Field(..., description="Name of the dataset, e.g., a file name.")
    created_by: Optional[str] = Field(None, description="ID of the user who created the dataset.")