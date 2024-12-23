import pickle
from sqlalchemy.dialects.postgresql import JSONB
from .engine import db
from core.rag.models.account import Account
from app.types.types import StringUUID
import json
from sqlalchemy.dialects.postgresql import JSONB

class Dataset(db.Model):
    __tablename__ = "datasets"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="dataset_pkey"),
        db.Index("dataset_tenant_idx", "tenant_id"),
    )

    id = db.Column(StringUUID, nullable=False, server_default=db.text("uuid_generate_v4()"))
    tenant_id = db.Column(StringUUID, nullable=False)
    dataset_id = db.Column(StringUUID, nullable=False)
    s3_path = db.Column(db.String(255))
    created_by = db.Column(StringUUID, nullable=False)
    index_struct = db.Column(JSONB, nullable=True)
    
    
    @property
    def created_by_account(self):
        return db.get(Account, self.created_by)
    
    @property
    def index_struct_dict(self):
        """Return index_struct as a Python dict, even if it's stored as a string."""
        if not self.index_struct:
            return None
        if isinstance(self.index_struct, str):
            # parse if needed
            return json.loads(self.index_struct)
        # already a dict
        return self.index_struct

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "created_by": self.created_by,
            "index_struct": self.index_struct,
        }

    @staticmethod
    def gen_collection_name_by_id(dataset_id: str) -> str:
        """Generate a collection name based on the dataset ID."""
        # Replace hyphens with underscores to ensure a valid SQL identifier
        cleaned_id = dataset_id.replace('-', '_')
        return f"collection_{cleaned_id}"

class Document(db.Model):
    __tablename__ = "documents"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="document_pkey"),
        db.Index("document_dataset_id_idx", "dataset_id"),
        db.Index("document_tenant_idx", "tenant_id"),
    )

    # initial fields
    id = db.Column(StringUUID, nullable=False, server_default=db.text("uuid_generate_v4()"))
    tenant_id = db.Column(StringUUID, nullable=False)
    dataset_id = db.Column(StringUUID, nullable=False)

    @property
    def dataset(self):
        return db.query(Dataset).filter(Dataset.id == self.dataset_id).first()

class Embedding(db.Model):
    __tablename__ = "embeddings"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="embedding_pkey"),
        db.Index("created_at_idx", "created_at"),
    )

    id = db.Column(StringUUID, primary_key=True, server_default=db.text("uuid_generate_v4()"))
    hash = db.Column(db.String(64), nullable=False)
    embedding = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP(0)"))
    provider_name = db.Column(db.String(255), nullable=False, server_default=db.text("''::character varying"))

    def set_embedding(self, embedding_data: list[float]):
        self.embedding = pickle.dumps(embedding_data, protocol=pickle.HIGHEST_PROTOCOL)

    def get_embedding(self) -> list[float]:
        return pickle.loads(self.embedding)