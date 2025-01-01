import uuid
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from repository.users import UserRepository
from configs import config
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repository: UserRepository, settings: config):
        self.user_repository = user_repository
        self.settings = settings

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM)

    def authenticate_user(self, email: str, password: str) -> Optional[str]:
        user = self.user_repository.get_user_by_email(email)
        if not user or not self.verify_password(password, user.password):
            return None
        token = self.create_access_token({"sub": user.email})
        return token

    def register_user(self, email: str, password: str, first_name: str, last_name: str):
        hashed_password = self.hash_password(password)
        tenant_id = uuid.uuid4()  
        return self.user_repository.create_user(
            email=email,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            tenant_id=tenant_id
        )

    def get_user_from_token(self, token: str):
        try:
            payload = jwt.decode(token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM])
            email = payload.get("sub")
            if email is None:
                return None
            return self.user_repository.get_user_by_email(email)
        except JWTError:
            return None
