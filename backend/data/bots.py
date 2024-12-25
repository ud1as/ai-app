from pydantic import BaseModel

class BotCreateRequest(BaseModel):
   name: str
   description: str

class BotConfigureRequest(BaseModel):
   prompt_template: str = """You are a helpful assistant trained to provide accurate information. Always be polite and professional.
   Context: {context}
   Question: {question}
   Instructions:
   - If the context provides relevant information, use it in your answer
   - If the context doesn't contain relevant information, let me know
   - Keep responses clear and concise
   - Be honest if you're not sure about something
   Answer:"""
   dataset_id: str

class MessageResponse(BaseModel):
   message: str
   
   
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str 
    relevant_context: str