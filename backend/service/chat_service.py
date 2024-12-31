from datetime import datetime
from typing import Dict, Optional
from core.memory.memory import TokenBufferMemoryMongoDB
from core.llm.openai_client import OpenAIClient
from service.dataset_retrieve import DatasetRetrievalService
from service.bot_service import BotService


DEFAULT_TENANT_ID = '00000000-0000-0000-0000-000000000001'

class ChatService:
   def __init__(self, memory: TokenBufferMemoryMongoDB, bot_service: BotService):
       self.memory = memory
       self.openai_client = OpenAIClient()
       self.retrieval_service = DatasetRetrievalService()
       self.bot_service = bot_service

   def get_relevant_context(self, dataset_id: str, query: str):
        try:
            results = self.retrieval_service.retrieve_documents(
                dataset_id=dataset_id,
                query=query,
                search_method="hybrid",
                top_k=3,
                score_threshold=0.6,
                hybrid_weights={"semantic": 0.5, "full_text": 0.5}
            )

            # Calculate and log the average score
            scores = [doc.metadata.get("score", 0) for doc in results]
            avg_score = sum(scores) / len(scores) if scores else 0
            print(f"[get_relevant_context] Average score of retrieved documents: {avg_score:.2f}")
            
            if avg_score < 0.5:
                print(f"[get_relevant_context] Average score below threshold, returning empty list")
                return []

            return results
        except Exception as e:
            print(f"[ERROR] Retrieval error for dataset_id {dataset_id}: {e}")
            return []

   def format_context(self, documents):
       if not documents:
           return ""
       context_parts = []
       for i, doc in enumerate(documents, 1):
           context_parts.append(f"Context {i}:\n{doc.page_content}\n")
       return "\n".join(context_parts)

   def format_messages_for_openai(self, messages, context: str = "", prompt_template: str = None):
       formatted_messages = [
           {"role": "system", "content": prompt_template} if prompt_template 
           else {"role": "system", "content": """You are a helpful assistant..."""}
       ]

       if context:
           formatted_messages.append({
               "role": "system",
               "content": f"Here's the relevant context:\n\n{context}"
           })

       for message in messages:
           formatted_messages.append({
               "role": message.role.value,
               "content": message.content
           })

       return formatted_messages

   def chat(self, bot_id: str, message: str, conversation_id: Optional[str] = None) -> Dict:
       try:
           bot = self.bot_service.get_bot(bot_id, DEFAULT_TENANT_ID)
           if not bot:
               raise ValueError(f"Bot with ID {bot_id} not found")
           
           if not conversation_id:
                conversation_id = f"{bot_id}-{datetime.utcnow().isoformat()}"

           config = self.bot_service.get_bot_config(bot_id)
           dataset_id = self.bot_service.get_dataset_id(bot_id)

           print(f"Bot config: {config}")
           print(f"Dataset ID: {dataset_id.dataset_id}")

            
           if not config:
               raise ValueError(f"Bot configuration for ID {bot_id} not found")
           if not dataset_id:
               raise ValueError(f"Dataset for bot ID {bot_id} not found")

           self.memory.save_message(conversation_id, {
               "role": "user",
               "query": message,
               "created_at": datetime.utcnow(),
           })

           relevant_docs = self.get_relevant_context(dataset_id.dataset_id, message)
           context = self.format_context(relevant_docs)

           messages = self.memory.get_messages(conversation_id, max_token_limit=2000)
           openai_messages = self.format_messages_for_openai(
               messages, 
               context,
               config.prompt_template
           )

           response = self.openai_client.generate_response(openai_messages)

           self.memory.save_message(conversation_id, {
               "role": "assistant",
               "answer": response,
               "created_at": datetime.utcnow(),
           })

           return {
               "response": response,
               "context": context,
               "conversation_id": conversation_id
           }

       except Exception as e:
           print(f"[ERROR] ChatService error for bot_id {bot_id}: {e}")
           raise e
