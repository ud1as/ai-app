from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from repository.ext_database import db


class App(db.Model):
    __tablename__ = "apps"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    datasets = relationship("AppDatasetJoin", back_populates="app")

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "created_by": str(self.created_by),
            "created_at": self.created_at.isoformat(),
        }


class Tag(db.Model):
    __tablename__ = "tags"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # Example: 'knowledge', 'category', etc.
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    bindings = relationship("TagBinding", back_populates="tag")

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "type": self.type,
            "tenant_id": str(self.tenant_id),
            "created_at": self.created_at.isoformat(),
        }


class TagBinding(db.Model):
    __tablename__ = "tag_bindings"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    tag_id = Column(UUID(as_uuid=True), ForeignKey("tags.id"), nullable=False)
    target_id = Column(UUID(as_uuid=True), nullable=False)  # E.g., dataset ID or another entity
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    tag = relationship("Tag", back_populates="bindings")

    def to_dict(self):
        return {
            "id": str(self.id),
            "tag_id": str(self.tag_id),
            "target_id": str(self.target_id),
            "tenant_id": str(self.tenant_id),
            "created_at": self.created_at.isoformat(),
        }


class UploadFile(db.Model):
    __tablename__ = "upload_files"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    name = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)  # File size in bytes
    extension = Column(String(50), nullable=False)  # File extension, e.g., 'txt', 'pdf'
    mime_type = Column(String(100), nullable=False)  # MIME type, e.g., 'application/pdf'
    created_by = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "size": self.size,
            "extension": self.extension,
            "mime_type": self.mime_type,
            "created_by": str(self.created_by),
            "created_at": self.created_at.isoformat(),
        }
