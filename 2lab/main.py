from fastapi import FastAPI, Depends
from app.api import auth_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User API",
    description="API для регистрации и аутентификации пользователей",
    openapi_tags=[{"name": "auth", "description": "Аутентификация и авторизация"}]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Сервер успешно запущен! Перейдите по ссылке http://127.0.0.1:8000/docs, чтобы посмотреть эндпоинт"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="User API",
        version="1.0.0",
        description="API для работы с пользователями",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/login/",
                    "scopes": {}
                }
            }
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
