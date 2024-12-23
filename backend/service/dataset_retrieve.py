# dataset_retrieve.py

import json
from typing import List, Optional

# Adjust these imports as needed for your codebase
from core.rag.models.dataset import Dataset  # or wherever your Dataset model actually resides
from core.rag.datasource.document import Document  # or wherever your Document class is defined
from repository.ext_database import db  # adjust path if needed

# This is your Vector wrapper that references PGVector or any other store:
from core.rag.datasource.vector_factory import Vector


class DatasetRetrievalService:
    """Service for retrieving relevant documents from a dataset."""

    def __init__(self):
        pass

    def retrieve_documents(
        self,
        dataset_id: str,
        query: str,
        search_method: str = "hybrid",
        top_k: int = 3,
        score_threshold: float = 0.5,
        hybrid_weights: Optional[dict] = None
    ) -> List[Document]:
        """
        Retrieve documents from a dataset by either semantic, full-text, or hybrid search.
        """
        try:
            dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
            if not dataset:
                print(f"[DatasetRetrievalService] No dataset found with id={dataset_id}")
                return []
            if isinstance(dataset.index_struct, str):
                dataset.index_struct = json.loads(dataset.index_struct)

            print("[DatasetRetrievalService] Creating Vector instance...")
            vector = Vector(dataset=dataset)

            if search_method == "semantic":
                print("[DatasetRetrievalService] Using semantic search...")
                results = vector.search_by_vector(
                    query=query,
                    top_k=top_k,
                    score_threshold=score_threshold
                )
                print("[DatasetRetrievalService] Got results from semantic search, now parsing metadata...")
                self._parse_metadata(results)

            elif search_method == "full_text":
                print("[DatasetRetrievalService] Using full_text search...")
                results = vector.search_by_full_text(query=query, top_k=top_k)
                print("[DatasetRetrievalService] Got results from full_text search, now parsing metadata...")
                self._parse_metadata(results)

            elif search_method == "hybrid":
                print("[DatasetRetrievalService] Using hybrid search...")
                semantic_results = vector.search_by_vector(
                    query=query,
                    top_k=top_k * 2,
                    score_threshold=score_threshold
                )
                full_text_results = vector.search_by_full_text(query=query, top_k=top_k * 2)

                print("[DatasetRetrievalService] Now parsing semantic_results metadata...")
                self._parse_metadata(semantic_results)
                print("[DatasetRetrievalService] Now parsing full_text_results metadata...")
                self._parse_metadata(full_text_results)

                results = self._combine_hybrid_results(
                    semantic_results,
                    full_text_results,
                    hybrid_weights or {"semantic": 0.5, "full_text": 0.5},
                    top_k
                )
            else:
                raise ValueError(f"Unsupported search method: {search_method}")

            print("[DatasetRetrievalService] Finished searches successfully. Here are the results:")
            for doc in results:
                print(f"    content={doc.page_content[:30]!r}..., metadata={doc.metadata}")

            return results

        except Exception as e:
            print(f"[DatasetRetrievalService] Error during document retrieval: {e}")
            return []

    @staticmethod
    def _combine_hybrid_results(
        semantic_results: List[Document],
        full_text_results: List[Document],
        weights: dict,
        top_k: int
    ) -> List[Document]:
        """
        Combine semantic and full-text search results with hybrid scoring.
        """
        doc_scores = {}

        for doc in semantic_results:
            meta = doc.metadata
            doc_id = meta.get("doc_id")
            score = meta.get("score", 0) * weights.get("semantic", 0.5)

            if doc_id is None:
                continue

            doc_scores[doc_id] = {"doc": doc, "score": score}

        for doc in full_text_results:
            meta = doc.metadata
            doc_id = meta.get("doc_id")
            score = meta.get("score", 0) * weights.get("full_text", 0.5)

            if doc_id is None:
                continue

            if doc_id in doc_scores:
                doc_scores[doc_id]["score"] += score
            else:
                doc_scores[doc_id] = {"doc": doc, "score": score}

        # Sort by combined score (descending)
        sorted_docs = sorted(doc_scores.values(), key=lambda x: x["score"], reverse=True)
        return [item["doc"] for item in sorted_docs[:top_k]]

    @staticmethod
    def _parse_metadata(docs: List[Document]) -> None:
        """
        Safely parse doc.metadata as JSON if it's a string, so doc.metadata.get() won't crash.
        
        
        """
        
        
        print(f"[DatasetRetrievalService] Parsing metadata for {len(docs)} : {docs} documents.")
        for doc in docs:
            if isinstance(doc.metadata, str):
                try:
                    doc.metadata = json.loads(doc.metadata)
                except json.JSONDecodeError:
                    doc.metadata = {}
