from typing import List
import openai
from core.rag.embedding.embedding_base import Embeddings
from configs.config import config

OPENAI_API_KEY = config.OPENAI_API_KEY
EMBEDDING_MODEL = config.EMBEDDING_MODEL

print(EMBEDDING_MODEL)

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


