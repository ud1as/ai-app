from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from configs.config import Settings
from core.llm.chat_assistant import ChatAssistant
from core.memory.memory import TokenBufferMemoryMongoDB
from handler.auth import AuthHandler
from handler.bots import BotHandler
from handler.knowledge import KnowledgeHandler
from repository.bots import BotRepository
from repository.ext_database import db
from repository.s3_storage import S3Storage
from repository.users import UserRepository
from service.auth import AuthService
from service.bot_service import BotService
from service.chat_service import ChatService
from service.file_service import FileService


def create_app():
    app = FastAPI(title="RAG System API")
    configs = Settings()

    # Initialize MongoDB client
    mongo_client = MongoClient(configs.MONGODB_URI)

    # Initialize services
    s3_storage = S3Storage(
        bucket_name=configs.S3_BUCKET,
        aws_access_key_id=configs.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=configs.AWS_SECRET_ACCESS_KEY,
        region_name=configs.AWS_REGION,
    )

    memory = TokenBufferMemoryMongoDB(
        client=mongo_client,
        db_name="rag_chat",
        collection_name="conversations",
    )

    file_service = FileService(s3_storage)
    chat_assistant = ChatAssistant(memory=memory)

    bot_repository = BotRepository(db)
    user_repository = UserRepository(db)

    bot_service = BotService(bot_repository)
    auth_service = AuthService(user_repository=user_repository, settings=configs)

    chat_service = ChatService(memory, bot_service)

    # Initialize handlers
    bot_handler = BotHandler(bot_service, chat_service)
    knowledge_handler = KnowledgeHandler(file_service, chat_assistant)
    auth_handler = AuthHandler(auth_service)

    # Add routers first
    app.include_router(bot_handler.router)
    app.include_router(knowledge_handler.router)
    app.include_router(auth_handler.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    return app
