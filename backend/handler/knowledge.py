from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from fastapi.responses import JSONResponse
from data import FilePreviewResponse, FileProcessResponse, FileProcessRequest, DatasetResponse, DatasetRequest
from service.file_service import FileService
from core.llm.chat_assistant import ChatAssistant
from typing import Optional, List
from app.utils.dependencies import get_current_user_tenant

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

    async def preview_file(
        self, 
        file: UploadFile = File(...),
        tenant_id: str = Depends(get_current_user_tenant)
    ):
        try:
            content = await file.read()
            success, chunks, error = self.file_service.get_chunk_preview(content, tenant_id)
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

    async def process_file(
        self, 
        file: UploadFile = File(...),
        tenant_id: str = Depends(get_current_user_tenant)
    ):
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

    async def get_datasets(
        self,
        tenant_id: str = Depends(get_current_user_tenant)
    ):
        try:
            datasets = self.file_service.get_datasets(tenant_id)
            return [DatasetResponse(**dataset) for dataset in datasets]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving datasets: {str(e)}")