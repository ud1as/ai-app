from datetime import datetime
from typing import Sequence, List, Tuple
from core.memory.memory import TokenBufferMemoryMongoDB
from core.llm.openai_client import OpenAIClient
from core.rag.retrieve.retrieval_service import RetrievalService, RetrievalMethod
from core.entities import PromptMessage
from core.rag.datasource.document import Document

class ChatAssistant:
    def __init__(self, memory: TokenBufferMemoryMongoDB):
        self.memory = memory
        self.openai_client = OpenAIClient()
        self.retrieval_service = RetrievalService()

    def get_relevant_context(self, dataset_id: str, query: str) -> List[Document]:
        """Get relevant documents using hybrid search."""
        return self.retrieval_service.retrieve(
            dataset_id=dataset_id,
            query=query,
            search_method=RetrievalMethod.HYBRID_SEARCH,
            top_k=3,
            score_threshold=0.5,
            hybrid_weights={'semantic': 0.7, 'full_text': 0.3}
        )

    def format_context(self, documents: List[Document]) -> str:
        """Format retrieved documents into context string."""
        if not documents:
            return ""
            
        context_parts = []
        for i, doc in enumerate(documents, 1):
            context_parts.append(f"Context {i}:\n{doc.page_content}\n")
        
        return "\n".join(context_parts)

    def format_messages_for_openai(
        self, 
        messages: Sequence[PromptMessage],
        context: str = ""
    ):
        # Start with system message including context
        system_message = """You are a virtual assistant named Alice. You are smart, friendly, and always ready to help. Your goal is to provide accurate and useful answers while explaining complex topics in simple terms. You communicate in a respectful and positive tone, keeping things easy to understand and approachable.

Your main responsibilities include:

Assisting with finding information, solving problems, and learning.
Supporting conversations to help the user achieve their goals.
Offering advice and recommendations based on the user’s context and preferences.
You primarily communicate in English but can switch to other languages if the user requests it. Your responses are clear and concise, but you can provide more detailed explanations when asked. You adapt your tone and style based on the user’s needs, whether they prefer a professional or casual approach.

You respect the user’s privacy and avoid asking unnecessary questions unless they are directly related to the task."""

        formatted_messages = [
            {"role": "system", "content": system_message}
        ]

        # Add context if available
        if context:
            formatted_messages.append({
                "role": "system",
                "content": f"Here's the relevant context to answer the question:\n\n{context}"
            })

        # Add conversation history
        for message in messages:
            formatted_messages.append({
                "role": message.role.value,
                "content": message.content
            })

        return formatted_messages

    def handle_message(
        self, 
        conversation_id: str, 
        user_message: str,
        dataset_id: str = None
    ) -> Tuple[str, str]:  # Return both response and context
        # Save user message
        self.memory.save_message(conversation_id, {
            "role": "user",
            "query": user_message,
            "created_at": datetime.utcnow(),
        })

        # Get relevant context if dataset_id is provided
        context = ""
        if dataset_id:
            relevant_docs = self.get_relevant_context(dataset_id, user_message)
            context = self.format_context(relevant_docs)
        # Get conversation history
        messages = self.memory.get_messages(conversation_id, max_token_limit=2000)
        
        # Format messages for OpenAI with context
        openai_messages = self.format_messages_for_openai(messages, context)
        
        # Get response from OpenAI
        response = self.openai_client.generate_response(openai_messages)
        
        # Save assistant response
        self.memory.save_message(conversation_id, {
            "role": "assistant",
            "answer": response,
            "created_at": datetime.utcnow(),
        })
        
        return response, context  # Return response and context
