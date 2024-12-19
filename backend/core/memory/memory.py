from typing import Optional, Sequence, List, Dict, Any
from pymongo import MongoClient
from pymongo.database import Database
from core.entities import (
    AssistantPromptMessage,
    PromptMessage,
    UserPromptMessage,
)
from datetime import datetime


class TokenBufferMemoryMongoDB:
    def __init__(self, client: MongoClient, db_name: str, collection_name: str) -> None:
        self.client = client
        self.db: Database = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_message(self, conversation_id: str, message: Dict[str, Any]) -> None:
        self.collection.insert_one({"conversation_id": conversation_id, **message})

    def get_messages(
        self,
        conversation_id: str,
        max_token_limit: int = 2000,
        message_limit: Optional[int] = None,
    ) -> Sequence[PromptMessage]:
        query = {"conversation_id": conversation_id}
        sort = [("created_at", -1)]

        cursor = self.collection.find(query).sort(sort)
        if message_limit:
            cursor = cursor.limit(message_limit)

        messages = list(cursor)
        messages.reverse()

        prompt_messages: List[PromptMessage] = []
        total_tokens = 0

        for msg in messages:
            if "query" in msg and msg.get("role") == "user":
                prompt_messages.append(UserPromptMessage(content=msg["query"]))
                total_tokens += len(msg["query"])
            if "answer" in msg and msg.get("role") == "assistant":
                prompt_messages.append(AssistantPromptMessage(content=msg["answer"]))
                total_tokens += len(msg["answer"])

            if total_tokens > max_token_limit:
                break

        return prompt_messages

    def get_history_prompt_text(
        self,
        conversation_id: str,
        human_prefix: str = "Human",
        ai_prefix: str = "Assistant",
        max_token_limit: int = 2000,
        message_limit: Optional[int] = None,
    ) -> str:
        prompt_messages = self.get_messages(
            conversation_id, max_token_limit=max_token_limit, message_limit=message_limit
        )

        string_messages = []
        for message in prompt_messages:
            if isinstance(message, UserPromptMessage):
                string_messages.append(f"{human_prefix}: {message.content}")
            elif isinstance(message, AssistantPromptMessage):
                string_messages.append(f"{ai_prefix}: {message.content}")

        return "\n".join(string_messages)
