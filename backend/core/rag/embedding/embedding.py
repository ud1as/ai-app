from typing import List
import openai
from core.rag.embedding.embedding_base import Embeddings
from configs.config import config

OPENAI_API_KEY = config.OPENAI_API_KEY
EMBEDDING_MODEL = config.EMBEDDING_MODEL

class OpenAIEmbedding(Embeddings):
    """OpenAI embedding implementation."""
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key is not set in configuration")
            
        self.client = openai.Client(api_key=OPENAI_API_KEY)
        self.model = EMBEDDING_MODEL
        self.dimension = 1536  # Dimension for text-embedding-3-small
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of documents."""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=texts,
                encoding_format="float"
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            raise Exception(f"Error generating document embeddings: {str(e)}")
            
    def embed_query(self, text: str) -> List[float]:
        """Generate embedding for a query text."""
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=[text],
                encoding_format="float"
            )
            return response.data[0].embedding
        except Exception as e:
            raise Exception(f"Error generating query embedding: {str(e)}")


def test_embedding():
    """Test function for OpenAI embeddings."""
    try:
        # Initialize embedding model
        print("Initializing OpenAI embedding model...")
        model = OpenAIEmbedding()
        
        # Test single query embedding
        print("\nTesting single query embedding...")
        query = "What is machine learning?"
        query_embedding = model.embed_query(query)
        print(f"Query embedding dimension: {len(query_embedding)}")
        print(f"First few values: {query_embedding[:3]}")
        
        # Test document embeddings
        print("\nTesting document embeddings...")
        documents = [
            "Machine learning is a branch of AI.",
            "Natural language processing is fascinating."
        ]
        doc_embeddings = model.embed_documents(documents)
        
        for i, (doc, embedding) in enumerate(zip(documents, doc_embeddings)):
            print(f"\nDocument {i+1}: {doc}")
            print(f"Embedding dimension: {len(embedding)}")
            print(f"First few values: {embedding[:3]}")
            
        print("\nAll tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"\nTest failed with error: {str(e)}")
        return False


if __name__ == "__main__":
    test_embedding()