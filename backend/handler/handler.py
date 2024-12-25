from fastapi import APIRouter, UploadFile, File, Depends, Form
from fastapi.responses import JSONResponse
from data import ChatRequest, FilePreviewResponse, FileProcessResponse, FileProcessRequest
from service.file_service import FileService
from core.llm.chat_assistant import ChatAssistant
from typing import Optional

router = APIRouter()

# Remove the global placeholder
file_service: FileService = None  # Will be injected
chat_assistant: ChatAssistant = None  # Will be injected

def register_routes(app, fs: FileService, ca: ChatAssistant):
    """Register all routes with the FastAPI app and inject dependencies."""
    global file_service, chat_assistant
    file_service = fs
    chat_assistant = ca
    app.include_router(router)

@router.post("/preview", response_model=FilePreviewResponse)
async def preview_file(
    file: UploadFile = File(...),
):
    """Preview file chunks."""
    try:
        content = await file.read()
        success, chunks, error = file_service.get_chunk_preview(content)
        if not success:
            return JSONResponse(status_code=400, content={"error": error})

        preview_data = [{
            'content': doc.page_content,
            'chunk_index': doc.metadata['chunk_index'],
            'chunk_total': doc.metadata['chunk_total']
        } for doc in chunks]

        return FilePreviewResponse(chunks=preview_data, total_chunks=len(chunks))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error previewing file: {str(e)}"})

@router.post("/process", response_model=FileProcessResponse)
async def process_file(
    file: UploadFile = File(...),
    tenant_id: str = Form(...)
):
    """
    Process file: upload to S3, create chunks, and store vectors.
    """
    try:
        # Read the file content
        file_content = await file.read()

        # Process the file using the file_service
        success, result = file_service.process_file(
            file_content=file_content,
            filename=file.filename,
            tenant_id=tenant_id
        )

        # Return response
        if success:
            return FileProcessResponse(success=True, dataset_id=result)
        else:
            return JSONResponse(status_code=400, content={"error": result})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error processing file: {str(e)}"})


@router.post("/chat")
async def chat(request: ChatRequest):
    """Chat endpoint with RAG support."""
    try:
        response, relevant_context = chat_assistant.handle_message(
            conversation_id=request.conversation_id,
            user_message=request.message,
            dataset_id=request.dataset_id
        )
        return {
            "response": response,
            "relevant_context": relevant_context,
            "conversation_id": request.conversation_id
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error processing message: {str(e)}"})
