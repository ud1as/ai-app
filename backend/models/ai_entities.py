from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


class ModelType(str):
    """
    Enum-like class for model type.
    """
    LLM = "llm"
    TEXT_EMBEDDING = "text-embedding"
    RERANK = "rerank"


class I18nObject(BaseModel):
    """
    Represents an internationalized object with support for multiple languages.
    """
    zh_Hans: Optional[str] = None
    en_US: str

    def __init__(self, **data):
        super().__init__(**data)
        if not self.zh_Hans:
            self.zh_Hans = self.en_US


class EmbeddingUsage(BaseModel):
    """
    Usage statistics for embedding models.
    """
    tokens: int
    total_tokens: int
    unit_price: Decimal
    price_unit: Decimal
    total_price: Decimal
    currency: str
    latency: float


class TextEmbeddingResult(BaseModel):
    """
    Result from embedding models.
    """
    model: str
    embeddings: list[list[float]]
    usage: EmbeddingUsage


class AIModel(BaseModel):
    """
    Represents a single AI model configuration.
    """
    model_name: str
    model_type: str
    description: Optional[str] = None
    price: Decimal