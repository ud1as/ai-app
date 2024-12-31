from typing import List, Optional
from models.bots import Bot, BotConfiguration, BotDataset
from sqlalchemy.orm import Session
from uuid import UUID


class BotRepository:
    def __init__(self, db_session: Session):
        """
        Initialize the repository with a SQLAlchemy database session.

        Args:
            db_session (Session): The SQLAlchemy session object.
        """
        self.db = db_session

    def get_by_id(self, bot_id: UUID, tenant_id: UUID) -> Optional[Bot]:
        """
        Retrieve a bot by its ID and tenant ID.

        Args:
            bot_id (UUID): The unique identifier of the bot.
            tenant_id (UUID): The tenant ID associated with the bot.

        Returns:
            Optional[Bot]: The bot object if found, or None otherwise.
        """
        try:
            return self.db.query(Bot).filter(
                Bot.id == bot_id,
                Bot.tenant_id == tenant_id
            ).first()
        except Exception as e:
            self.db.rollback()
            raise e

    def create(self, bot: Bot) -> Bot:
        """
        Create a new bot in the database.

        Args:
            bot (Bot): The bot object to create.

        Returns:
            Bot: The newly created bot.
        """
        try:
            print("I am here")
            self.db.add(bot)
            self.db.commit()
            self.db.refresh(bot)
            return bot
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_tenant(self, tenant_id: UUID) -> List[Bot]:
        """
        Retrieve all bots for a specific tenant.

        Args:
            tenant_id (UUID): The tenant ID.

        Returns:
            List[Bot]: A list of bots associated with the tenant.
        """
        try:
            return self.db.query(Bot).filter(Bot.tenant_id == tenant_id).all()
        except Exception as e:
            self.db.rollback()
            raise e

    def get_config(self, bot_id: UUID) -> Optional[BotConfiguration]:
        """
        Retrieve the configuration for a specific bot.

        Args:
            bot_id (UUID): The unique identifier of the bot.

        Returns:
            Optional[BotConfiguration]: The bot configuration if found, or None otherwise.
        """
        try:
            return self.db.query(BotConfiguration).filter(
                BotConfiguration.bot_id == bot_id
            ).first()
        except Exception as e:
            self.db.rollback()
            raise e

    def save_config(self, config: BotConfiguration) -> None:
        """
        Save or update a bot's configuration.

        Args:
            config (BotConfiguration): The bot configuration to save.
        """
        try:
            self.db.add(config)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def get_dataset(self, bot_id: UUID) -> Optional[BotDataset]:
        """
        Retrieve the dataset for a specific bot.

        Args:
            bot_id (UUID): The unique identifier of the bot.

        Returns:
            Optional[BotDataset]: The bot dataset if found, or None otherwise.
        """
        try:
            return self.db.query(BotDataset).filter(
                BotDataset.bot_id == bot_id
            ).first()
        except Exception as e:
            self.db.rollback()
            raise e

    def save_dataset(self, dataset: BotDataset) -> None:
        """
        Save or update a bot's dataset.

        Args:
            dataset (BotDataset): The bot dataset to save.
        """
        try:
            self.db.add(dataset)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def configure(self, bot_id: UUID, prompt_template: str, dataset_id: UUID) -> bool:
        """
        Configure a bot by updating its prompt template and dataset.

        Args:
            bot_id (UUID): The unique identifier of the bot.
            prompt_template (str): The prompt template for the bot.
            dataset_id (UUID): The dataset ID associated with the bot.

        Returns:
            bool: True if the configuration was successful.
        """
        try:
            # Update or create the bot configuration
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

            # Update or create the bot dataset
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
        except Exception as e:
            self.db.rollback()
            raise e
