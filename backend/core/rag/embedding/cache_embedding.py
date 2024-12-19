# core/rag/embedding/cache_embedding.py

from typing import List
import hashlib
import pickle
from .embedding_base import Embeddings
from repository.ext_database import db
from core.rag.models.dataset import Embedding 

class CacheEmbedding(Embeddings): 
    """Caching wrapper for embeddings."""
    
    def __init__(self, embedding_model: Embeddings):
        self.embedding_model = embedding_model
        
    def _get_hash(self, text: str) -> str:
        """Generate hash for text."""
        return hashlib.sha256(text.encode()).hexdigest()
    
    def _get_cached_embedding(self, text_hash: str) -> List[float] | None:
        """Retrieve embedding from cache."""
        cached = db.query(Embedding).filter_by(hash=text_hash).first()
        if cached:
            return cached.get_embedding()
        return None
    
    def _cache_embedding(self, text_hash: str, embedding_data: List[float]):
        """Store embedding in cache."""
        embedding = Embedding(
            model_name=self.embedding_model.model,
            hash=text_hash,
        )
        embedding.set_embedding(embedding_data)
        db.add(embedding)
        db.commit()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for documents with caching."""
        results = []
        texts_to_embed = []
        text_hashes = []
        
        for text in texts:
            text_hash = self._get_hash(text)
            cached = self._get_cached_embedding(text_hash)
            
            if cached:
                results.append(cached)
            else:
                texts_to_embed.append(text)
                text_hashes.append(text_hash)
        
        if texts_to_embed:
            new_embeddings = self.embedding_model.embed_documents(texts_to_embed)
            for i, embedding in enumerate(new_embeddings):
                self._cache_embedding(text_hashes[i], embedding)
                results.append(embedding)
                
        return results
    
    def embed_query(self, text: str) -> List[float]:
        """Get embedding for query with caching."""
        text_hash = self._get_hash(text)
        cached = self._get_cached_embedding(text_hash)
        
        if cached:
            return cached
            
        embedding = self.embedding_model.embed_query(text)
        self._cache_embedding(text_hash, embedding)
        return embedding