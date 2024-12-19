import json
import uuid
from contextlib import contextmanager
from typing import Any, List

import psycopg2.extras
import psycopg2.pool
from pydantic import BaseModel, model_validator

from configs.config import config
from core.rag.datasource.vector_base import AbstractVectorFactory, BaseVector
from core.rag.datasource.vector_type import VectorType
from core.rag.embedding.embedding_base import Embeddings
from core.rag.datasource.document import Document
from core.rag.models.dataset import Dataset


class PGVectorConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str
    min_connection: int
    max_connection: int

    @model_validator(mode="before")
    @classmethod
    def validate_config(cls, values: dict) -> dict:
        if not values["host"]:
            raise ValueError("config PGVECTOR_HOST is required")
        if not values["port"]:
            raise ValueError("config PGVECTOR_PORT is required")
        if not values["user"]:
            raise ValueError("config PGVECTOR_USER is required")
        if not values["password"]:
            raise ValueError("config PGVECTOR_PASSWORD is required")
        if not values["database"]:
            raise ValueError("config PGVECTOR_DATABASE is required")
        if not values["min_connection"]:
            raise ValueError("config PGVECTOR_MIN_CONNECTION is required")
        if not values["max_connection"]:
            raise ValueError("config PGVECTOR_MAX_CONNECTION is required")
        if values["min_connection"] > values["max_connection"]:
            raise ValueError("config PGVECTOR_MIN_CONNECTION should be less than PGVECTOR_MAX_CONNECTION")
        return values


SQL_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS {table_name} (
    id UUID PRIMARY KEY,
    text TEXT NOT NULL,
    meta JSONB NOT NULL,
    embedding vector({dimension}) NOT NULL
) using heap;
"""


class PGVector(BaseVector):
    def __init__(self, collection_name: str, config: PGVectorConfig):
        super().__init__(collection_name)
        self.pool = self._create_connection_pool(config)
        self.table_name = f"embedding_{collection_name}"

    def get_type(self) -> str:
        return VectorType.PGVECTOR

    def _create_connection_pool(self, config: PGVectorConfig):
        return psycopg2.pool.SimpleConnectionPool(
            config.min_connection,
            config.max_connection,
            host=config.host,
            port=config.port,
            user=config.user,
            password=config.password,
            database=config.database,
        )

    @contextmanager
    def _get_cursor(self):
        conn = self.pool.getconn()
        cur = conn.cursor()
        try:
            yield cur
        finally:
            cur.close()
            conn.commit()
            self.pool.putconn(conn)

    def create(self, texts: list[Document], embeddings: list[list[float]], **kwargs):
        dimension = len(embeddings[0])
        print(f"Creating collection with dimension {dimension}...")
        self._create_collection(dimension)
        print("Adding texts to vector store...")
        return self.add_texts(texts, embeddings)


    def add_texts(self, documents: list[Document], embeddings: list[list[float]], **kwargs):
        values = []
        pks = []

        for i, doc in enumerate(documents):
            doc_id = str(uuid.uuid4())  # Generate unique ID
            pks.append(doc_id)

            # Convert the embedding list into PostgreSQL vector format
            formatted_embedding = f"[{', '.join(map(str, embeddings[i]))}]"
            values.append(
                (
                    doc_id,
                    doc.page_content,
                    json.dumps(doc.metadata),
                    formatted_embedding,
                )
            )

        with self._get_cursor() as cur:
            try:
                psycopg2.extras.execute_values(
                    cur,
                    f"INSERT INTO {self.table_name} (id, text, meta, embedding) VALUES %s",
                    values,
                    template="(%s, %s, %s, %s::vector)",
                )
            except Exception as e:
                print(f"Error inserting texts into database: {e}")
                raise
        return pks


    def text_exists(self, id: str) -> bool:
        with self._get_cursor() as cur:
            cur.execute(f"SELECT id FROM {self.table_name} WHERE id = %s", (id,))
            return cur.fetchone() is not None

    def get_by_ids(self, ids: list[str]) -> list[Document]:
        with self._get_cursor() as cur:
            cur.execute(f"SELECT meta, text FROM {self.table_name} WHERE id IN %s", (tuple(ids),))
            docs = []
            for record in cur:
                docs.append(Document(page_content=record[1], metadata=record[0]))
        return docs

    def delete_by_ids(self, ids: list[str]) -> None:
        with self._get_cursor() as cur:
            cur.execute(f"DELETE FROM {self.table_name} WHERE id IN %s", (tuple(ids),))

    def delete_by_metadata_field(self, key: str, value: str) -> None:
        with self._get_cursor() as cur:
            cur.execute(f"DELETE FROM {self.table_name} WHERE meta->>%s = %s", (key, value))

    def search_by_vector(self, query_vector: list[float], **kwargs: Any) -> list[Document]:
        """
        Search the nearest neighbors to a vector.

        :param query_vector: The input vector to search for similar items.
        :param top_k: The number of nearest neighbors to return, default is 5.
        :return: List of Documents that are nearest to the query vector.
        """
        top_k = kwargs.get("top_k", 4)

        with self._get_cursor() as cur:
            cur.execute(
                f"SELECT meta, text, embedding <=> %s AS distance FROM {self.table_name}"
                f" ORDER BY distance LIMIT {top_k}",
                (query_vector,),
            )
            docs = []
            score_threshold = float(kwargs.get("score_threshold") or 0.0)
            for record in cur:
                metadata, text, distance = record
                score = 1 - distance
                metadata["score"] = score
                if score > score_threshold:
                    docs.append(Document(page_content=text, metadata=metadata))
        return docs

    def search_by_full_text(self, query: str, **kwargs: Any) -> list[Document]:
        top_k = kwargs.get("top_k", 5)

        with self._get_cursor() as cur:
            cur.execute(
                f"""SELECT meta, text, ts_rank(to_tsvector(coalesce(text, '')), plainto_tsquery(%s)) AS score
                FROM {self.table_name}
                WHERE to_tsvector(text) @@ plainto_tsquery(%s)
                ORDER BY score DESC
                LIMIT {top_k}""",
                (query, query),
            )

            docs = []

            for record in cur:
                metadata, text, score = record
                metadata["score"] = score
                docs.append(Document(page_content=text, metadata=metadata))

        return docs

    def delete(self) -> None:
        with self._get_cursor() as cur:
            cur.execute(f"DROP TABLE IF EXISTS {self.table_name}")

    def _create_collection(self, dimension: int):
        with self._get_cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            cur.execute(SQL_CREATE_TABLE.format(table_name=self.table_name, dimension=dimension))


class PGVectorFactory(AbstractVectorFactory):
    def init_vector(self, dataset: Dataset, attributes: list, embeddings: Embeddings) -> PGVector:
        if dataset.index_struct_dict:
            class_prefix: str = dataset.index_struct_dict["vector_store"]["class_prefix"]
            collection_name = class_prefix
        else:
            dataset_id = dataset.id
            collection_name = Dataset.gen_collection_name_by_id(dataset_id)
            dataset.index_struct = json.dumps(self.gen_index_struct_dict(VectorType.PGVECTOR, collection_name))

        return PGVector(
            collection_name=collection_name,
            config=PGVectorConfig(
                host=config.PGVECTOR_HOST,
                port=config.PGVECTOR_PORT,
                user=config.PGVECTOR_USER,
                password=config.PGVECTOR_PASSWORD,
                database=config.PGVECTOR_DATABASE,
                min_connection=config.PGVECTOR_MIN_CONNECTION,
                max_connection=config.PGVECTOR_MAX_CONNECTION,
            ),
        )
