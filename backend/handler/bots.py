from fastapi import APIRouter, HTTPException
from data.bots import BotCreateRequest, BotConfigureRequest, MessageResponse, ChatRequest, ChatResponse

DEFAULT_TENANT_ID = '00000000-0000-0000-0000-000000000001'

class BotHandler:
   def __init__(self, bot_service, chat_service):
       self.bot_service = bot_service
       self.chat_service = chat_service
       self.router = APIRouter(prefix="/api/bots", tags=["bots"])
       self.setup_routes()

   def setup_routes(self):
       self.router.post("", response_model=MessageResponse)(self.create_bot)
       self.router.get("")(self.get_bots)
       self.router.get("/{bot_id}")(self.get_bot)
       self.router.post("/{bot_id}/configure", response_model=MessageResponse)(self.configure_bot)
       self.router.post("/{bot_id}/chat", response_model=ChatResponse)(self.chat)

   def create_bot(self, bot_data: BotCreateRequest):
       try:
           bot = self.bot_service.create_bot(
               name=bot_data.name,
               description=bot_data.description,
               tenant_id=DEFAULT_TENANT_ID
           )
           return MessageResponse(message="Bot successfully created")
       except Exception as e:
           raise HTTPException(status_code=400, detail=str(e))

   def get_bots(self):
       try:
           bots = self.bot_service.get_bots(DEFAULT_TENANT_ID)
           return [bot.to_dict() for bot in bots]
       except Exception as e:
           raise HTTPException(status_code=400, detail=str(e))

   def get_bot(self, bot_id: str):
       try:
           bot = self.bot_service.get_bot(bot_id, DEFAULT_TENANT_ID)
           if not bot:
               raise HTTPException(status_code=404, detail="Bot not found")
           return bot.to_dict()
       except Exception as e:
           raise HTTPException(status_code=400, detail=str(e))

   def configure_bot(self, bot_id: str, config: BotConfigureRequest):
       try:
           self.bot_service.configure_bot(
               bot_id=bot_id,
               prompt_template=config.prompt_template,
               dataset_id=config.dataset_id,
               tenant_id=DEFAULT_TENANT_ID
           )
           return MessageResponse(message="Bot successfully configured")
       except Exception as e:
           raise HTTPException(status_code=400, detail=str(e))

   def chat(self, bot_id: str, request: ChatRequest):
       try:
           bot = self.bot_service.get_bot(bot_id, DEFAULT_TENANT_ID)
           if not bot:
               raise HTTPException(status_code=404, detail="Bot not found")

           response = self.chat_service.chat(
               bot_id=bot_id,
               message=request.query
           )
           
           return ChatResponse(
               answer=response["response"],
               relevant_context=response["context"]
           )
       except Exception as e:
           raise HTTPException(status_code=400, detail=str(e))