from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Header
from fastapi.responses import JSONResponse
from data import FilePreviewResponse, FileProcessResponse, FileProcessRequest, DatasetResponse, DatasetRequest
from service.file_service import FileService
from core.llm.chat_assistant import ChatAssistant
from typing import Optional, List

DEFAULT_TENANT_ID = '00000000-0000-0000-0000-000000000001'

class KnowledgeHandler:
    def __init__(self, file_service: FileService, chat_assistant: ChatAssistant):
        self.file_service = file_service
        self.chat_assistant = chat_assistant
        self.router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])
        self.setup_routes()

    def setup_routes(self):
        self.router.post("/preview", response_model=FilePreviewResponse)(self.preview_file)
        self.router.post("/process", response_model=FileProcessResponse)(self.process_file)
        self.router.get("/datasets", response_model=List[DatasetResponse])(self.get_datasets)

    async def preview_file(self, file: UploadFile = File(...)):
        """Preview file chunks."""
        try:
            content = await file.read()
            success, chunks, error = self.file_service.get_chunk_preview(content)
            if not success:
                raise HTTPException(status_code=400, detail=error)

            preview_data = [{
                'content': doc.page_content,
                'chunk_index': doc.metadata['chunk_index'],
                'chunk_total': doc.metadata['chunk_total']
            } for doc in chunks]

            return FilePreviewResponse(chunks=preview_data, total_chunks=len(chunks))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error previewing file: {str(e)}")

    async def process_file(self, file: UploadFile = File(...), tenant_id: str = Form(DEFAULT_TENANT_ID)):
        """
        Process file: upload to S3, create chunks, and store vectors.
        """
        try:
            file_content = await file.read()

            success, result = self.file_service.process_file(
                file_content=file_content,
                filename=file.filename,
                tenant_id=tenant_id
            )

            if success:
                return FileProcessResponse(success=True, dataset_id=result)
            else:
                raise HTTPException(status_code=400, detail=result)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    async def get_datasets(self):
        try:
            datasets = self.file_service.get_all_datasets(DEFAULT_TENANT_ID)
            return [DatasetResponse(**dataset) for dataset in datasets]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving datasets: {str(e)}")

# Usage example
# file_service and chat_assistant need to be instantiated and injected into this handler.
# app = FastAPI()
# knowledge_handler = KnowledgeHandler(file_service, chat_assistant)
# app.include_router(knowledge_handler.router)
