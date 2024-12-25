from typing import List, Optional
from models.bots import Bot, BotConfiguration, BotDataset
from sqlalchemy.orm import Session

class BotRepository:
    def __init__(self, db_session):
        self.db = db_session

    def get_by_id(self, bot_id: str, tenant_id: str):
        try:
            result = self.db.query(Bot).filter(
                Bot.id == bot_id,
                Bot.tenant_id == tenant_id
            ).first()
            self.db.commit()
            return result
        except:
            self.db.rollback()
            raise

    def create(self, bot: Bot) -> Bot:
       self.db.add(bot)
       self.db.commit()
       self.db.refresh(bot)
       return bot

    def get_by_tenant(self, tenant_id: str) -> List[Bot]:
       return self.db.query(Bot).filter(Bot.tenant_id == tenant_id).all()

    def get_by_id(self, bot_id: str, tenant_id: str) -> Optional[Bot]:
       return self.db.query(Bot).filter(Bot.id == bot_id, Bot.tenant_id == tenant_id).first()

    def get_config(self, bot_id: str) -> Optional[BotConfiguration]:
       return self.db.query(BotConfiguration).filter(BotConfiguration.bot_id == bot_id).first()

    def save_config(self, config: BotConfiguration) -> None:
       self.db.add(config)
       self.db.commit()

    def get_dataset(self, bot_id: str) -> Optional[BotDataset]:
       return self.db.query(BotDataset).filter(BotDataset.bot_id == bot_id).first()

    def save_dataset(self, dataset: BotDataset) -> None:
       self.db.add(dataset)
       self.db.commit()
       
    def configure(self, bot_id: str, prompt_template: str, dataset_id: str):
        try:
            config = self.db.query(BotConfiguration).filter(
                BotConfiguration.bot_id == bot_id
            ).first()
            
            if config:
                config.prompt_template = prompt_template
            else:
                config = BotConfiguration(
                    bot_id=bot_id,
                    prompt_template=prompt_template
                )
                self.db.add(config)
            
            dataset = self.db.query(BotDataset).filter(
                BotDataset.bot_id == bot_id
            ).first()

            if dataset:
                dataset.dataset_id = dataset_id
            else:
                dataset = BotDataset(bot_id=bot_id, dataset_id=dataset_id)
                self.db.add(dataset)

            self.db.commit()
            return True
        except:
            self.db.rollback()
            raise
