from sqlalchemy.orm import Session
from models.users import User
import uuid


class UserRepository:
    def __init__(self, db=Session):
        self.db = db

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, email: str, password: str, first_name: str, last_name: str, tenant_id: uuid.UUID):
        new_user = User(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            tenant_id=tenant_id,
            is_active=True,
            is_admin=False
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

