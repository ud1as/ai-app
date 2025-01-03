from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.authentication import BaseUser



class FastAPIUser(BaseUser):
    def __init__(self, user_id: int, first_name: str, last_name: str):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name

    @property
    def is_authenticated(self) -> bool:
        return True

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, auth_service):
        super().__init__(app)
        self.auth_service = auth_service

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/api/auth/login", "/open-endpoint", "/api/auth/register"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return JSONResponse({"error": "Authorization header missing"}, status_code=401)

        try:
            token = auth_header.split(" ")[1]
            user_info = self.auth_service.get_user_info_from_token(token)
            if not user_info:
                return JSONResponse({"error": "Invalid or expired token"}, status_code=401)

            request.state.user = FastAPIUser(
                user_id=user_info["user_id"],
                first_name=user_info["first_name"],
                last_name=user_info["last_name"]
            )
            request.state.scopes = user_info["scopes"]
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=401)

        return await call_next(request)
