from abc import ABC, abstractmethod
from typing import List

class Embeddings(ABC):
    """Base class for text embeddings."""
    
    @abstractmethod
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search documents."""
        pass
    
    @abstractmethod
    def embed_query(self, text: str) -> List[float]:
        """Embed query text."""
        pass