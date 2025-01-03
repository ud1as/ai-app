from fastapi import APIRouter, HTTPException, Depends, status
from service.auth import AuthService
from data import UserRegisterRequest, UserLoginRequest, UserResponse
from app.utils.dependencies import oauth2_scheme

class AuthHandler:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.router = APIRouter(prefix="/api/auth", tags=["auth"])
        self.setup_routes()

    def setup_routes(self):
        self.router.post("/register", response_model=UserResponse)(self.register_user)
        self.router.post("/login")(self.login_user)
        self.router.get("/me", response_model=UserResponse)(self.get_current_user)

    async def register_user(self, user_data: UserRegisterRequest):
        try:
            return self.auth_service.register_user(
                email=user_data.email,
                password=user_data.password,
                first_name=user_data.first_name,
                last_name=user_data.last_name
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def login_user(self, user_data: UserLoginRequest):
        try:
            token = self.auth_service.authenticate_user(
                email=user_data.email,
                password=user_data.password
            )
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            return {"access_token": token, "token_type": "bearer"}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        try:
            user = self.auth_service.get_user_from_token(token)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid token")
            return user
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))