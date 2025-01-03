from typing import Tuple, List
import uuid
from repository.s3_storage import S3Storage
from core.rag.datasource.vector_factory import Vector
from core.rag.datasource.document import Document
from core.rag.text_splitter.text_splitter import TextSplitter
from repository.ext_database import db
from repository.file import DatasetRepository
from core.rag.models.dataset import Dataset

class FileService:
    def __init__(self, s3_storage: S3Storage):
        self.s3_storage = s3_storage
        self.dataset_repository = DatasetRepository 
        self.text_splitter = TextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def preview_chunks(self, file_content: str, tenant_id: str) -> List[Document]:
        try:
            base_metadata = {
                "source": "preview",
                "preview": True,
                "tenant_id": tenant_id
            }
            
            documents = self.text_splitter.split_documents(
                text=file_content,
                metadata=base_metadata
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

            s3_success = self.s3_storage.save(s3_filename, file_content)
            if not s3_success:
                return False, "Failed to save file to S3"

            dataset = Dataset(
                name=filename,
                dataset_id=file_id,
                s3_path=s3_filename,
                tenant_id=tenant_id
            )

            db.add(dataset)
            db.commit()

            base_metadata = {
                "source": filename,
                "dataset_id": dataset.id,
                "tenant_id": tenant_id
            }
            
            documents = self.text_splitter.split_documents(
                text=file_content.decode('utf-8'),
                metadata=base_metadata
            )
            
            for doc in documents:
                doc.metadata["doc_id"] = str(uuid.uuid4())
                doc.metadata["tenant_id"] = tenant_id

            vector = Vector(dataset=dataset)
            vector.create(documents)

            return True, dataset.id

        except Exception as e:
            db.rollback()
            return False, str(e)

    def get_chunk_preview(self, file_content: bytes, tenant_id: str) -> Tuple[bool, List[Document], str]:
        try:
            text_content = file_content.decode('utf-8')
            chunks = self.preview_chunks(text_content, tenant_id)
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
                self.s3_storage.delete(dataset.s3_path)
                self.dataset_repository.delete(dataset_id)
                return True
            return False
        except Exception as e:
            print(f"Error deleting dataset: {e}")
            return False