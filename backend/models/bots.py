from .engine import db
from app.types.types import StringUUID
from sqlalchemy.dialects.postgresql import JSONB

class Bot(db.Model):
    __tablename__ = "bots"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="bot_pkey"),
        db.Index("bot_tenant_idx", "tenant_id"),
    )

    id = db.Column(StringUUID, nullable=False, server_default=db.text("uuid_generate_v4()"))
    tenant_id = db.Column(StringUUID, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "tenant_id": self.tenant_id,
            "name": self.name,
            "description": self.description
        }

class BotConfiguration(db.Model):
    __tablename__ = "bot_configurations"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="bot_config_pkey"),
        db.Index("bot_config_bot_idx", "bot_id"),
    )

    id = db.Column(StringUUID, nullable=False, server_default=db.text("uuid_generate_v4()"))
    bot_id = db.Column(StringUUID, nullable=False)
    prompt_template = db.Column(db.Text, nullable=False)
    system_prompt = db.Column(db.Text, nullable=True)
    temperature = db.Column(db.Float, default=0.7)
    max_tokens = db.Column(db.Integer, default=1000)
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP(0)"))

    @property
    def bot(self):
        return db.query(Bot).filter(Bot.id == self.bot_id).first()

class BotDataset(db.Model):
    __tablename__ = "bot_datasets"
    __table_args__ = (
        db.PrimaryKeyConstraint("bot_id", "dataset_id", name="bot_dataset_pkey"),
        db.Index("bot_dataset_bot_idx", "bot_id"),
        db.Index("bot_dataset_dataset_idx", "dataset_id"),
    )

    bot_id = db.Column(StringUUID, nullable=False)
    dataset_id = db.Column(StringUUID, nullable=False)

class BotUsage(db.Model):
    __tablename__ = "bot_usage"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="bot_usage_pkey"),
        db.Index("bot_usage_bot_idx", "bot_id"),
    )

    id = db.Column(StringUUID, nullable=False, server_default=db.text("uuid_generate_v4()"))
    bot_id = db.Column(StringUUID, nullable=False)
    total_messages = db.Column(db.Integer, default=0)

    @property
    def bot(self):
        return db.query(Bot).filter(Bot.id == self.bot_id).first()