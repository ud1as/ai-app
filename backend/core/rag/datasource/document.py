from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Optional, List
from pydantic import BaseModel, Field

class Document(BaseModel):
    """Class for storing a piece of text and associated metadata."""
    
    page_content: str
    vector: Optional[List[float]] = None
    metadata: Optional[dict] = Field(default_factory=dict)
    provider: Optional[str] = "flitchat"

class BaseDocumentTransformer(ABC):
    """Abstract base class for document transformation systems."""
    
    @abstractmethod
    def transform_documents(
        self, 
        documents: Sequence[Document], 
        **kwargs: Any
    ) -> Sequence[Document]:
        """Transform a list of documents."""
        raise NotImplementedError
    
    @abstractmethod
    async def atransform_documents(
        self, 
        documents: Sequence[Document], 
        **kwargs: Any
    ) -> Sequence[Document]:
        """Asynchronously transform a list of documents."""
        raise NotImplementedError