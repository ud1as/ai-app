# core/rag/text_splitter/text_splitter.py

from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.rag.datasource.document import Document

class TextSplitter:
    """Text splitter service for chunking documents."""
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: List[str] = ["\n\n", "\n", " ", ""]
    ):
            
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators
        )

    def split_text(self, text: str) -> List[str]:
        """Split text into chunks."""
        return self.text_splitter.split_text(text)
    
    def split_documents(self, text: str, metadata: dict = None) -> List[Document]:
        """Split text and create Document objects."""
        chunks = self.split_text(text)
        documents = []
        
        for i, chunk in enumerate(chunks):
            # Extend metadata with chunk information
            chunk_metadata = {
                **(metadata or {}),
                "chunk_index": i,
                "chunk_total": len(chunks)
            }
            
            documents.append(Document(
                page_content=chunk,
                metadata=chunk_metadata
            ))
            
        return documents