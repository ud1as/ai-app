from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from handler.handler import register_routes, file_service, chat_assistant
from core.memory.memory import TokenBufferMemoryMongoDB
from core.llm.chat_assistant import ChatAssistant
from service.file_service import FileService
from configs.config import Settings
from repository.s3_storage import S3Storage

def create_app():
    """Initialize and configure the FastAPI app."""
    app = FastAPI(title="RAG System API")

    # Configure CORS
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

    mongo_client = MongoClient(configs.MONGODB_URI)
    memory = TokenBufferMemoryMongoDB(
        client=mongo_client,
        db_name="rag_chat",
        collection_name="conversations"
    )

    # Initialize dependencies
    file_service = FileService(s3_storage)
    chat_assistant = ChatAssistant(memory=memory)

    # Register routes with injected dependencies
    register_routes(app, file_service, chat_assistant)

    return app
