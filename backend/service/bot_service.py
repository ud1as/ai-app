from models.bots import Bot, BotConfiguration, BotDataset
from repository.bots import BotRepository
from typing import List, Optional

class BotService:
    def __init__(self, bot_repository: BotRepository):
       self.repository = bot_repository

    def create_bot(self, name: str, description: str, tenant_id: str) -> Bot:
       bot = Bot(name=name, description=description, tenant_id=tenant_id)
       return self.repository.get_by_tenant(tenant_id)

    def get_bot(self, bot_id: str, tenant_id: str) -> Optional[Bot]:
       return self.repository.get_by_id(bot_id, tenant_id)

    def configure_bot(self, bot_id: str, prompt_template: str, dataset_id: str, tenant_id: str) -> Bot:
       bot = self.repository.get_by_id(bot_id, tenant_id)
       if not bot:
           raise ValueError("Bot not found")

       config = self.repository.get_config(bot_id)
       
       if config:
           config.prompt_template = prompt_template
       else:
           config = BotConfiguration(bot_id=bot_id, prompt_template=prompt_template)
       self.repository.save_config(config)

       dataset = self.repository.get_dataset(bot_id)
       if dataset:
           dataset.dataset_id = dataset_id
       else:
           dataset = BotDataset(bot_id=bot_id, dataset_id=dataset_id)
       self.repository.save_dataset(dataset)

       return bot
   
    def get_bot_config(self, bot_id: str) -> Optional[BotConfiguration]:
        return self.repository.get_config(bot_id)
    
    def get_dataset_id(self, bot_id: str) -> Optional[BotDataset]:
        return self.repository.get_dataset(bot_id)