import uuid
from pathlib import Path
from typing import List, Tuple

from core.rag.datasource.vector_factory import Vector
from core.rag.extractor.extract_processor import ExtractProcessor
from core.rag.models.dataset import Dataset
from core.rag.models.document import Document
from core.rag.models.model import UploadFile
from core.rag.text_splitter.text_splitter import TextSplitter
from repository.ext_database import db
from repository.file import DatasetRepository
from repository.s3_storage import S3Storage


class FileService:
    def __init__(self, s3_storage: S3Storage):
        self.storage = s3_storage
        self.dataset_repository = DatasetRepository
        self.text_splitter = TextSplitter(chunk_size=1000, chunk_overlap=200)
        self.extract_processor = ExtractProcessor(storage=self.storage)

    def preview_chunks(self, file_content: str, tenant_id: str) -> List[Document]:
        try:
            base_metadata = {
                "source": "preview",
                "preview": True,
                "tenant_id": tenant_id,
            }

            documents = self.text_splitter.split_documents(
                text=file_content, metadata=base_metadata
            )

            return documents
        except Exception as e:
            print(f"Chunking error: {str(e)}")
            return []

    def process_file(
        self,
        file_content: bytes,
        filename: str,
        tenant_id: str,
    ) -> Tuple[bool, str]:
        try:
            file_id = str(uuid.uuid4())
            s3_filename = f"{tenant_id}/{file_id}_{filename}"

            # Save file to S3
            s3_success = self.storage.save(s3_filename, file_content)
            if not s3_success:
                return False, "Failed to save file to S3"

            # Create dataset record
            dataset = Dataset(
                name=filename,
                dataset_id=file_id,
                s3_path=s3_filename,
                tenant_id=tenant_id,
            )

            db.add(dataset)
            db.commit()

            # Create upload file object for extractor
            upload_file = UploadFile(
                key=s3_filename,
                name=filename,
            )

            # Extract text using ExtractProcessor
            documents = self.extract_processor.load_from_upload_file(
                upload_file=upload_file, return_text=True
            )

            base_metadata = {
                "source": filename,
                "dataset_id": dataset.id,
                "tenant_id": tenant_id,
            }

            chunks: List[Document] = []
            for document in documents:
                chunk = self.text_splitter.split_documents(
                    text=document.page_content, metadata=base_metadata
                )

                chunks.extend(chunk)

            for chunk in chunks:
                chunk.metadata["doc_id"] = str(uuid.uuid4())
                chunk.metadata["tenant_id"] = tenant_id

            # Create vector embeddings
            vector = Vector(dataset=dataset)
            vector.create(chunks)

            return True, dataset.id

        except Exception as e:
            db.rollback()
            return False, str(e)

    def get_chunk_preview(
        self, file_content: bytes, tenant_id: str, filename: str
    ) -> Tuple[bool, List[Document], str]:
        try:
            # Create temporary file and upload file object
            file_id = str(uuid.uuid4())
            suffix = Path(filename).suffix
            temp_filename = f"preview_{file_id}{suffix}"
            s3_filename = f"{tenant_id}/preview/{temp_filename}"

            # Save temporarily to S3
            s3_success = self.storage.save(s3_filename, file_content)
            if not s3_success:
                return False, [], "Failed to save preview file"

            upload_file = UploadFile(
                key=s3_filename,
                name=filename,
            )

            # Extract text using ExtractProcessor
            documents = self.extract_processor.load_from_upload_file(
                upload_file=upload_file, return_text=False
            )

            base_metadata = {
                "source": "preview",
                "preview": True,
                "tenant_id": tenant_id,
            }

            chunks: List[Document] = []
            for document in documents:
                chunk = self.text_splitter.split_documents(
                    text=document.page_content, metadata=base_metadata
                )

                chunks.extend(chunk)

            # Clean up preview file
            self.storage.delete(s3_filename)

            return True, chunks, ""

        except Exception as e:
            return False, [], str(e)

    def get_datasets(self, tenant_id: str) -> List[dict]:
        try:
            return self.dataset_repository.get_datasets_by_tenant(tenant_id)
        except Exception as e:
            print(f"Error retrieving datasets: {e}")
            return []

    def delete_dataset(self, dataset_id: str, tenant_id: str) -> bool:
        try:
            dataset = self.dataset_repository.get_by_id(dataset_id)
            if dataset and dataset.tenant_id == tenant_id:
                self.storage.delete(dataset.s3_path)
                self.dataset_repository.delete(dataset_id)
                return True
            return False
        except Exception as e:
            print(f"Error deleting dataset: {e}")
            return False
