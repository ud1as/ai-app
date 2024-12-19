import json
import pickle
from sqlalchemy import (
    Column,
    String,
    Text,
    DateTime,
    Integer,
    func,
    PrimaryKeyConstraint,
    Index,
    text,
    LargeBinary
)
from repository.ext_database import Base, db
from core.rag.models.account import Account
from app.types.types import StringUUID
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector as VECTOR

class Dataset(Base):
    __tablename__ = "datasets"
    __table_args__ = (
        Index("dataset_tenant_idx", "tenant_id"),
        {"extend_existing": True}
    )

    id = Column(StringUUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    tenant_id = Column(StringUUID, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    s3_path = Column(String(255))
    created_by = Column(StringUUID, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP(0)"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP(0)"))
    index_struct = Column(JSONB, nullable=True)  # Vector metadata

    @property
    def created_by_account(self):
        return db.get(Account, self.created_by)

    @property
    def document_count(self):
        from core.rag.models.dataset import Document
        return db.query(func.count(Document.id)).filter(Document.dataset_id == self.id).scalar()

    @property
    def index_struct_dict(self):
        # Safely return the JSON structure as a dict
        return self.index_struct if self.index_struct else None

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "document_count": self.document_count,
            "index_struct": self.index_struct,
        }

    @staticmethod
    def gen_collection_name_by_id(dataset_id: str) -> str:
        """Generate a collection name based on the dataset ID."""
        # Replace hyphens with underscores to ensure a valid SQL identifier
        cleaned_id = dataset_id.replace('-', '_')
        return f"collection_{cleaned_id}"

class Document(Base):
    __tablename__ = "documents"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="document_pkey"),
        Index("document_dataset_id_idx", "dataset_id"),
    )

    id = Column(StringUUID, server_default=text("uuid_generate_v4()"))
    dataset_id = Column(StringUUID, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP(0)"))

    @property
    def dataset(self):
        return db.query(Dataset).filter(Dataset.id == self.dataset_id).first()

class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True)
    model_name = Column(String(255), nullable=False)
    hash = Column(String(64), nullable=False)
    embedding = Column(VECTOR(1536), nullable=False)  # Define as VECTOR(1536)

    def set_embedding(self, embedding_data: list[float]):
        """Directly set the embedding as a list of floats."""
        self.embedding = embedding_data

    def get_embedding(self) -> list[float]:
        """Retrieve the embedding as a list of floats."""
        return self.embedding