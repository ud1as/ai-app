# core/rag/retrieval/retrieval_service.py

from typing import List, Optional
from core.rag.datasource.document import Document
from core.rag.datasource.vector_factory import Vector
from core.rag.models.dataset import Dataset
from repository.ext_database import db

class RetrievalMethod:
    SEMANTIC_SEARCH = "semantic_search"
    FULL_TEXT_SEARCH = "full_text_search"
    HYBRID_SEARCH = "hybrid_search"

class RetrievalService:
    @staticmethod
    def retrieve(
        dataset_id: str,
        query: str,
        search_method: str,
        top_k: int = 4,
        score_threshold: float = 0.0,
        hybrid_weights: Optional[dict] = None
    ) -> List[Document]:
        """
        Retrieve documents using semantic, full-text, or hybrid search.
        
        Args:
            dataset_id: ID of the dataset to search
            query: Search query
            search_method: Type of search to perform
            top_k: Number of results to return
            score_threshold: Minimum similarity score (0-1)
            hybrid_weights: Weights for hybrid search {
                'semantic': float, 
                'full_text': float
            }
            
        Returns:
            List of Document objects
        """
        # Input validation
        if not query or not dataset_id:
            return []

        # Get dataset
        dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
        if not dataset:
            return []

        try:
            # Initialize vector store
            vector = Vector(dataset=dataset)
            
            # Clean query
            cleaned_query = RetrievalService._clean_query(query)
            
            if search_method == RetrievalMethod.HYBRID_SEARCH:
                return RetrievalService._hybrid_search(
                    vector=vector,
                    query=cleaned_query,
                    top_k=top_k,
                    score_threshold=score_threshold,
                    weights=hybrid_weights or {'semantic': 0.5, 'full_text': 0.5}
                )
            
            elif search_method == RetrievalMethod.SEMANTIC_SEARCH:
                return vector.search_by_vector(
                    query=cleaned_query,
                    top_k=top_k,
                    score_threshold=score_threshold
                )
                
            elif search_method == RetrievalMethod.FULL_TEXT_SEARCH:
                return vector.search_by_full_text(
                    query=cleaned_query,
                    top_k=top_k
                )
                
            else:
                raise ValueError(f"Unsupported search method: {search_method}")

        except Exception as e:
            print(f"Error during retrieval: {str(e)}")
            return []

    @staticmethod
    def _hybrid_search(
        vector: Vector,
        query: str,
        top_k: int,
        score_threshold: float,
        weights: dict
    ) -> List[Document]:
        """
        Perform hybrid search combining semantic and full-text search results.
        
        Args:
            vector: Vector store instance
            query: Search query
            top_k: Number of results to return
            score_threshold: Minimum similarity score
            weights: Weights for each search type
            
        Returns:
            Combined and reranked list of documents
        """
        # Get results from both methods
        semantic_docs = vector.search_by_vector(
            query=query,
            top_k=top_k * 2,  # Get more results for better combination
            score_threshold=score_threshold
        )
        
        full_text_docs = vector.search_by_full_text(
            query=query,
            top_k=top_k * 2
        )
        
        # Combine results with weighted scores
        doc_scores = {}
        
        # Process semantic search results
        for doc in semantic_docs:
            doc_id = doc.metadata.get('doc_id')
            score = doc.metadata.get('score', 0) * weights['semantic']
            doc_scores[doc_id] = {
                'doc': doc,
                'score': score
            }
        
        # Process full-text search results
        for doc in full_text_docs:
            doc_id = doc.metadata.get('doc_id')
            full_text_score = doc.metadata.get('score', 0) * weights['full_text']
            
            if doc_id in doc_scores:
                # Add full-text score to existing document
                doc_scores[doc_id]['score'] += full_text_score
            else:
                # Add new document
                doc_scores[doc_id] = {
                    'doc': doc,
                    'score': full_text_score
                }
        
        # Sort by combined score and get top_k results
        sorted_docs = sorted(
            doc_scores.values(),
            key=lambda x: x['score'],
            reverse=True
        )[:top_k]
        
        # Update metadata with combined scores
        results = []
        for item in sorted_docs:
            doc = item['doc']
            doc.metadata['score'] = item['score']
            results.append(doc)
        
        return results

    @staticmethod
    def _clean_query(query: str) -> str:
        """Clean and prepare query for search."""
        return query.replace('"', '\\"').strip()