from uuid import UUID
from typing import List, Optional
from models.bots import Bot, BotConfiguration, BotDataset
from repository.bots import BotRepository


class BotService:
    def __init__(self, bot_repository: BotRepository):
        self.repository = bot_repository

    def create_bot(self, name: str, description: str, tenant_id: str) -> Bot:
        tenant_uuid = UUID(tenant_id)  # Convert tenant_id to UUID
        bot = Bot(name=name, description=description, tenant_id=tenant_uuid)
        return self.repository.create(bot)

    def get_bot(self, bot_id: str, tenant_id: str) -> Optional[Bot]:
        bot_uuid = UUID(bot_id)  # Convert bot_id to UUID
        tenant_uuid = UUID(tenant_id)  # Convert tenant_id to UUID
        return self.repository.get_by_id(bot_uuid, tenant_uuid)
    
    def get_bots(self, tenant_id: str) -> List[Bot]:
        """
        Retrieve all bots associated with a specific tenant.
        """
        tenant_uuid = UUID(tenant_id)  # Convert tenant_id to UUID
        return self.repository.get_by_tenant(tenant_uuid)

    def configure_bot(
        self, bot_id: str, prompt_template: str, dataset_id: str, tenant_id: str
    ) -> Bot:
        bot_uuid = UUID(bot_id)  # Convert bot_id to UUID
        tenant_uuid = UUID(tenant_id)  # Convert tenant_id to UUID

        bot = self.repository.get_by_id(bot_uuid, tenant_uuid)
        if not bot:
            raise ValueError("Bot not found")

        config = self.repository.get_config(bot_uuid)

        if config:
            config.prompt_template = prompt_template
        else:
            config = BotConfiguration(bot_id=bot_uuid, prompt_template=prompt_template)
        self.repository.save_config(config)

        dataset = self.repository.get_dataset(bot_uuid)
        if dataset:
            dataset.dataset_id = dataset_id
        else:
            dataset = BotDataset(bot_id=bot_uuid, dataset_id=dataset_id)
            self.repository.save_dataset(dataset)

        return bot

    def get_bot_config(self, bot_id: str) -> Optional[BotConfiguration]:
        bot_uuid = UUID(bot_id)  # Convert bot_id to UUID
        return self.repository.get_config(bot_uuid)

    def get_dataset_id(self, bot_id: str) -> Optional[BotDataset]:
        bot_uuid = UUID(bot_id)  # Convert bot_id to UUID
        return self.repository.get_dataset(bot_uuid)
