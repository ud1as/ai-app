from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    conversation_id: str
    dataset_id: Optional[str] = None
