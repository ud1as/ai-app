from datetime import datetime
from typing import Sequence, List, Tuple
from core.memory.memory import TokenBufferMemoryMongoDB
from core.llm.openai_client import OpenAIClient
from core.rag.retrieve.retrieval_service import RetrievalService, RetrievalMethod
from core.entities import PromptMessage
from pymongo import MongoClient
from core.rag.datasource.document import Document
from configs.config import config
from service.dataset_retrieve import DatasetRetrievalService

class ChatAssistant:
    def __init__(self, memory: TokenBufferMemoryMongoDB):
        self.memory = memory
        self.openai_client = OpenAIClient()
        self.retrieval_service = DatasetRetrievalService()

    def get_relevant_context(self, dataset_id: str, query: str) -> List[Document]:
        """Get relevant documents using hybrid search."""
        try:
            results = self.retrieval_service.retrieve_documents(
                dataset_id=dataset_id,
                query=query,
                search_method="hybrid",
                top_k=3,
                score_threshold=0.5,
                hybrid_weights={"semantic": 0.5, "full_text": 0.5}
            )
            print(f"Retrieved results: {results}")
            return results
        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []


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

    def test_get_relevant_context(self, dataset_id: str, query: str):
        """Test the get_relevant_context function."""
        try:
            print(f"Testing get_relevant_context with dataset_id={dataset_id} and query='{query}'")
            documents = self.get_relevant_context(dataset_id, query)
            if documents:
                print("Relevant documents retrieved:")
                for i, doc in enumerate(documents, 1):
                    print(f"Document {i}:")
                    print(f"Content: {doc.page_content}")
                    print(f"Metadata: {doc.metadata}")
            else:
                print("No relevant documents found.")
        except Exception as e:
            print(f"Error during test: {e}")

# Example usage
if __name__ == "__main__":
    mongo_client = MongoClient(config.MONGODB_URI)
    memory = TokenBufferMemoryMongoDB(
    client=mongo_client,
    db_name="rag_chat",
    collection_name="conversations"
)
    assistant = ChatAssistant(memory=memory)

    # Example test for get_relevant_context
    test_dataset_id = "4e003dc7-31f7-4b42-a238-5b7f298d71bb"
    test_query = "Almaty?"
    assistant.test_get_relevant_context(dataset_id=test_dataset_id, query=test_query)
