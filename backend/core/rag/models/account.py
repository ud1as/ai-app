import enum
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AccountStatus(str, enum.Enum):
    """
    Enumeration for account status.
    """
    ACTIVE = "active"
    PENDING = "pending"
    CLOSED = "closed"
    BANNED = "banned"


class Account(Base):
    """
    Simplified Account model for basic account management.
    """
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    status = Column(String(16), nullable=False, server_default=text("'active'"))
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_login_at = Column(DateTime, nullable=True)
    last_login_ip = Column(String(255), nullable=True)

    def to_dict(self) -> dict:
        """
        Convert the account instance to a dictionary.
        """
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "avatar": self.avatar,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login_at": self.last_login_at.isoformat() if self.last_login_at else None,
            "last_login_ip": self.last_login_ip,
        }
