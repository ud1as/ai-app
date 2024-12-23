import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
from pymongo import MongoClient
import uvicorn


# Import core components
from core.memory.memory import TokenBufferMemoryMongoDB
from core.llm.chat_assistant import ChatAssistant
from core.rag.retrieve.retrieval_service import RetrievalService, RetrievalMethod
from core.rag.text_splitter.text_splitter import TextSplitter
from repository.s3_storage import S3Storage
from service.file_service import FileService
from configs.config import Settings
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse




class ChatRequest(BaseModel):
    message: str
    conversation_id: str
    dataset_id: Optional[str] = None

# Initialize FastAPI app
app = FastAPI(title="RAG System API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load configuration
configs = Settings()

# Initialize services
s3_storage = S3Storage(
    bucket_name=configs.S3_BUCKET,
    aws_access_key_id=configs.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=configs.AWS_SECRET_ACCESS_KEY,
    region_name=configs.AWS_REGION
)

# Initialize MongoDB and memory
mongo_client = MongoClient(configs.MONGODB_URI)
memory = TokenBufferMemoryMongoDB(
    client=mongo_client,
    db_name="rag_chat",
    collection_name="conversations"
)

# Initialize services
file_service = FileService(s3_storage)
chat_assistant = ChatAssistant(memory=memory)
retrieval_service = RetrievalService()


@app.post("/preview")
async def preview_file(
    file: UploadFile = File(...),
    chunk_size: Optional[int] = Form(1000),
    chunk_overlap: Optional[int] = Form(200)
):
    """
    Preview file chunks before processing
    """
    try:
        # Read file content once
        content = await file.read()
        
        # Get chunks preview by passing the content directly
        success, chunks, error = file_service.get_chunk_preview(content)
        
        if not success:
            return JSONResponse(
                status_code=400,
                content={"error": error}
            )
        
        # Convert chunks to displayable format
        preview_data = [{
            'content': doc.page_content,
            'chunk_index': doc.metadata['chunk_index'],
            'chunk_total': doc.metadata['chunk_total']
        } for doc in chunks]
        
        return {
            'chunks': preview_data,
            'total_chunks': len(chunks)
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error processing file: {str(e)}"}
        )

@app.post("/process")
async def process_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    tenant_id: str = Form(...),  # Require tenant_id
    created_by: str = Form(...),  # Require created_by
    chunk_size: Optional[int] = Form(1000),
    chunk_overlap: Optional[int] = Form(200)
):
    """
    Process file: upload to S3, create chunks, and store vectors
    """
    try:
        # Read file content once
        file_content = await file.read()

        # Pass file content and metadata to the service
        success, result = file_service.process_file(
            file_content=file_content,  # Pass file content
            filename=file.filename,     # Pass filename
            description=description,
            tenant_id=tenant_id,        # Pass tenant_id
            created_by=created_by,      # Pass created_by
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        if success:
            return {
                'success': True,
                'dataset_id': result
            }
        else:
            return JSONResponse(
                status_code=400,
                content={
                    'success': False,
                    'error': result
                }
            )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                'success': False,
                'error': f"Error processing file: {str(e)}"
            }
        )





@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint with RAG support
    """
    try:
        # Generate response and retrieve context
        response, relevant_context = chat_assistant.handle_message(
            conversation_id=request.conversation_id,
            user_message=request.message,
            dataset_id=request.dataset_id
        )
        
        return {
            "response": response,
            "relevant_context": relevant_context,  # Include retrieved context
            "conversation_id": request.conversation_id
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error processing message: {str(e)}"})


@app.post("/search")
async def search_documents(
    query: str,
    dataset_id: str,
    search_method: str = RetrievalMethod.HYBRID_SEARCH,
    top_k: int = 4,
    score_threshold: float = 0.5
):
    """
    Search documents in the dataset
    """
    try:
        documents = retrieval_service.retrieve(
            dataset_id=dataset_id,
            query=query,
            search_method=search_method,
            top_k=top_k,
            score_threshold=score_threshold,
            hybrid_weights={'semantic': 0.7, 'full_text': 0.3}
        )
        
        results = [{
            'content': doc.page_content,
            'metadata': doc.metadata,
            'score': doc.metadata.get('score', 0)
        } for doc in documents]
        
        return {
            'results': results,
            'total': len(results)
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error searching documents: {str(e)}"}
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )