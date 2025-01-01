from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from handler.bots import BotHandler
from handler.knowledge import KnowledgeHandler
from handler.auth import AuthHandler

from core.memory.memory import TokenBufferMemoryMongoDB
from core.llm.chat_assistant import ChatAssistant
from service.auth import AuthService

from service.file_service import FileService
from service.bot_service import BotService
from service.chat_service import ChatService

from configs.config import Settings

from repository.s3_storage import S3Storage
from repository.ext_database import db
from repository.bots import BotRepository
from repository.users import UserRepository


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
        region_name=configs.AWS_REGION,
    )

    mongo_client = MongoClient(configs.MONGODB_URI)
    memory = TokenBufferMemoryMongoDB(
        client=mongo_client,
        db_name="rag_chat",
        collection_name="conversations",
    )

    # Initialize dependencies
    file_service = FileService(s3_storage)
    chat_assistant = ChatAssistant(memory=memory)

    bot_repository = BotRepository(db)
    user_repository = UserRepository(db)

    bot_service = BotService(bot_repository)
    auth_service = AuthService(user_repository, configs)

    chat_service = ChatService(memory, bot_service)

    bot_handler = BotHandler(bot_service, chat_service)
    knowledge_handler = KnowledgeHandler(file_service, chat_assistant)
    auth_handler = AuthHandler(auth_service)

    # Include routers
    app.include_router(bot_handler.router)
    app.include_router(knowledge_handler.router)
    app.include_router(auth_handler.router)

    return app
