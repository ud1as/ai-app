from datetime import datetime
from core.memory.memory import TokenBufferMemoryMongoDB
from core.llm.openai_client import OpenAIClient
from typing import Sequence
from core.entities import PromptMessage

class ChatAssistant:
    def __init__(self, memory: TokenBufferMemoryMongoDB):
        self.memory = memory
        self.openai_client = OpenAIClient()

    def format_messages_for_openai(self, messages: Sequence[PromptMessage]):
        formatted_messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        
        for message in messages:
            formatted_messages.append({
                "role": message.role.value,
                "content": message.content
            })
            
        return formatted_messages

    def handle_message(self, conversation_id: str, user_message: str) -> str:
        # Save user message
        self.memory.save_message(conversation_id, {
            "role": "user",
            "query": user_message,
            "created_at": datetime.utcnow(),
        })

        # Get conversation history using existing method
        messages = self.memory.get_messages(conversation_id, max_token_limit=2000)
        
        # Format messages for OpenAI
        openai_messages = self.format_messages_for_openai(messages)

        # Get response from OpenAI
        response = self.openai_client.generate_response(openai_messages)

        # Save assistant response
        self.memory.save_message(conversation_id, {
            "role": "assistant",
            "answer": response,
            "created_at": datetime.utcnow(),
        })

        return response