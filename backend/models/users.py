from .engine import db
from app.types.types import StringUUID
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, Integer, Index, text

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = (
        db.PrimaryKeyConstraint("id", name="user_pkey"),
        db.Index("user_email_idx", "email"),
        db.Index("user_tenant_idx", "tenant_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, server_default=text("TRUE"))
    is_admin = Column(Boolean, default=False, server_default=text("FALSE"))
    tenant_id = Column(UUID(as_uuid=True), nullable=False)

    def to_dict(self):
        """Convert the user instance to a dictionary for easy serialization."""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            "tenant_id": str(self.tenant_id)
        }
