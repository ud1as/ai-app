# vector_factory.py

from abc import ABC, abstractmethod
from typing import Optional, Any
import json


from core.rag.datasource.pgvector import PGVectorFactory
from core.rag.datasource.vector_base import BaseVector
from core.rag.datasource.vector_type import VectorType
from core.rag.embedding.cache_embedding import CacheEmbedding
from core.rag.embedding.embedding_base import Embeddings
from core.rag.models.document import Document
from core.rag.models.dataset import Dataset
from core.rag.embedding.embedding import OpenAIEmbedding
from core.rag.embedding.cache_embedding import CacheEmbedding
from repository.ext_database import db


class AbstractVectorFactory(ABC):
    @abstractmethod
    def init_vector(self, dataset: Dataset, attributes: list, embeddings: Embeddings) -> BaseVector:
        raise NotImplementedError

    @staticmethod
    def gen_index_struct_dict(vector_type: VectorType, collection_name: str) -> dict:
        index_struct_dict = {"type": vector_type.value, "vector_store": {"class_prefix": collection_name}}
        return index_struct_dict


class Vector:
    """Vector store implementation using PGVector."""
    def __init__(self, dataset: Dataset, attributes: Optional[list] = None):
        if attributes is None:
            attributes = ["doc_id", "dataset_id", "document_id", "doc_hash"]
        self._dataset = dataset
        self._embeddings = self._get_embeddings()
        self._attributes = attributes
        self._vector_processor = self._init_vector()
        
    def _get_embeddings(self) -> Embeddings:
        """
        Initialize and return the embedding model.
        """
        base_embedding = OpenAIEmbedding()  # Initialize OpenAIEmbedding
        cached_embedding = CacheEmbedding(base_embedding)
        return cached_embedding

    def _init_vector(self) -> BaseVector:
        """Safely initialize PGVector instance."""
        vector_type = VectorType.PGVECTOR
        dataset_id = self._dataset.id

        if not self._dataset.index_struct:
            # Generate a new index structure if it doesn't exist
            collection_name = Dataset.gen_collection_name_by_id(dataset_id)
            index_struct = {
                "type": vector_type.value,
                "vector_store": {"class_prefix": collection_name},
            }
            # Directly assign the dictionary; JSONB will handle storage
            self._dataset.index_struct = index_struct
            db.add(self._dataset)
            db.commit()
        else:
            # Directly use the dictionary
            index_struct = self._dataset.index_struct
            collection_name = index_struct["vector_store"]["class_prefix"]

        # Initialize the PGVector processor
        return PGVectorFactory().init_vector(self._dataset, self._attributes, self._embeddings)

    def create(self, texts: Optional[list] = None, **kwargs):
        """Create vector embeddings for texts."""
        if texts is None or not all(isinstance(t, Document) for t in texts):
            raise ValueError("texts must be a list of Document instances")

        embeddings = self._embeddings.embed_documents([document.page_content for document in texts])
        
        self._vector_processor.create(texts=texts, embeddings=embeddings, **kwargs)

    def add_texts(self, documents: list[Document], **kwargs):
        """Add new documents to vector store."""
        if not all(isinstance(doc, Document) for doc in documents):
            raise ValueError("documents must be a list of Document instances")

        if kwargs.get("duplicate_check", False):
            documents = self._filter_duplicate_texts(documents)

        embeddings = self._embeddings.embed_documents([document.page_content for document in documents])
        
        self._vector_processor.create(texts=documents, embeddings=embeddings, **kwargs)

    def text_exists(self, id: str) -> bool:
        """Check if a text exists in vector store."""
        return self._vector_processor.text_exists(id)

    def delete_by_ids(self, ids: list[str]) -> None:
        """Delete documents by their IDs."""
        self._vector_processor.delete_by_ids(ids)

    def delete_by_metadata_field(self, key: str, value: str) -> None:
        """Delete documents by metadata field."""
        self._vector_processor.delete_by_metadata_field(key, value)

    def search_by_vector(self, query: str, top_k=3, score_threshold=0.5) -> list[Document]:
        print("[Vector] Starting search_by_vector...")
        query_vector = self._embeddings.embed_query(query)

        docs = self._vector_processor.search_by_vector(query_vector, top_k=top_k)
        print(f"[Vector] _vector_processor returned {len(docs)} docs.")

        filtered_docs = []
        for i, doc in enumerate(docs):
            # Debug print:
            print(f"[Vector] Before parse => doc {i} metadata type={type(doc.metadata)}, value={doc.metadata}")
            if isinstance(doc.metadata, str):
                try:
                    doc.metadata = json.loads(doc.metadata)
                except json.JSONDecodeError:
                    doc.metadata = {}

            # Potential threshold check
            if doc.metadata.get("score", 0) >= score_threshold:
                filtered_docs.append(doc)
        
        print(f"[Vector] Returning {len(filtered_docs)} docs after threshold filtering.")
        return filtered_docs


    def search_by_full_text(self, query: str, **kwargs: Any) -> list[Document]:
        """Search documents by full text."""
        # This might return docs with string metadata, so we do not do threshold checks here.
        # We'll let the service parse the metadata or do any threshold checks if needed.
        return self._vector_processor.search_by_full_text(query, **kwargs)

    def delete(self) -> None:
        """Delete the vector store."""
        self._vector_processor.delete()

    def _filter_duplicate_texts(self, texts: list[Document]) -> list[Document]:
        """Filter out duplicate documents."""
        for text in texts.copy():
            doc_id = text.metadata["doc_id"]
            if self.text_exists(doc_id):
                texts.remove(text)
        return texts

    def __getattr__(self, name):
        if name in ("_vector_processor", "_embeddings"):
            raise AttributeError(f"{name} attribute not initialized")

        if hasattr(self, "_vector_processor") and self._vector_processor:
            method = getattr(self._vector_processor, name, None)
            if callable(method):
                return method
        raise AttributeError(f"'vector_processor' object has no attribute '{name}'")
