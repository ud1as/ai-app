from typing import Tuple, List
import uuid
from repository.s3_storage import S3Storage
from core.rag.datasource.vector_factory import Vector
from core.rag.datasource.document import Document
from core.rag.text_splitter.text_splitter import TextSplitter
from repository.ext_database import db
from core.rag.models.dataset import Dataset
DEFAULT_TENANT_ID = "00000000-0000-0000-0000-000000000001"  # Replace with a valid UUID
SYSTEM_USER_ID = "00000000-0000-0000-0000-000000000002"      # Replace with a valid UUID

class FileService:
    def __init__(self, s3_storage: S3Storage):
        self.s3_storage = s3_storage
        self.text_splitter = TextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def preview_chunks(self, file_content: str) -> List[Document]:
        """Preview text chunks before vectorization."""
        try:
            # Create base metadata
            base_metadata = {
                "source": "preview",
                "preview": True
            }
            
            # Split into documents with metadata
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
        tenant_id: str = None,  # Add tenant_id
    ) -> Tuple[bool, str]:
        try:
            print("Starting file processing...")
            file_id = str(uuid.uuid4())
            print(f"File ID: {file_id}")

            s3_filename = f"{file_id}_{filename}"
            print(f"Saving to S3: {s3_filename}")

            # Save to S3
            s3_success = self.s3_storage.save(s3_filename, file_content)
            if not s3_success:
                print("Failed to save to S3")
                return False, "Failed to save file to S3"

            print("Inserting into database...")
            print("Creating dataset object...")
            dataset = Dataset(
                dataset_id=file_id,
                s3_path=s3_filename,
                tenant_id=tenant_id or DEFAULT_TENANT_ID
            )
            print(f"Dataset object created: {dataset.to_dict()}")

            print("Adding dataset to the database...")
            db.add(dataset)

            print("Committing to the database...")
            db.commit()
            print("Pass")

            print(f"Dataset ID: {dataset.id}")

            base_metadata = {
                "source": filename,
                "dataset_id": dataset.id
            }
            documents = self.text_splitter.split_documents(
                text=file_content.decode('utf-8'),
                metadata=base_metadata
            )
            for i, doc in enumerate(documents):
    # Add a unique doc_id for each chunk, e.g. dataset_id + chunk index
                doc.metadata["doc_id"] = str(uuid.uuid4())

            print("Creating vector embeddings...")
            vector = Vector(dataset=dataset)
            vector.create(documents)

            print("File processed successfully.")
            return True, dataset.id

        except Exception as e:
            db.rollback()
            print(f"Commit failed: {e}")
            print(f"Error: {e}")
            return False, str(e)






    def get_chunk_preview(self, file_content: bytes) -> Tuple[bool, List[Document], str]:
        """Get preview of chunks before processing."""
    
        try:
            # Decode content to text
            text_content = file_content.decode('utf-8')
            
            # Get chunks preview
            chunks = self.preview_chunks(text_content)
            
            return True, chunks, ""
            
        except Exception as e:
            return False, [], str(e)
