from fastapi import APIRouter, HTTPException, Header, Depends, status
from pydantic import BaseModel
from typing import Optional
from service.auth import AuthService
from data import UserRegisterRequest, UserLoginRequest, UserResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

class AuthHandler:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.router = APIRouter(prefix="/api/auth", tags=["auth"])
        self.setup_routes()

    def setup_routes(self):
        self.router.post("/register", response_model=UserResponse)(self.register_user)
        self.router.post("/login")(self.login_user)
        self.router.get("/me", response_model=UserResponse)(self.get_current_user)

    def register_user(self, user_data: UserRegisterRequest):
        """
        Endpoint for user registration.
        """
        try:
            user = self.auth_service.register_user(
                email=user_data.email,
                password=user_data.password,
                first_name=user_data.first_name,
                last_name=user_data.last_name
            )
            return user
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def login_user(self, request: UserLoginRequest):
        """
        Endpoint for user login using JSON body.
        """
        try:
            token = self.auth_service.authenticate_user(
                email=request.email,
                password=request.password
            )
            if not token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
            return {"access_token": token, "token_type": "bearer"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_current_user(self, token: str = Depends(oauth2_scheme)):
        """
        Retrieve details of the current authenticated user.
        """
        try:
            user = self.auth_service.get_user_from_token(token)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid token or user not found")
            return user
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
