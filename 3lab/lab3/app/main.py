from fastapi import FastAPI
from app.api.auth import auth_router
from app.websocket.routes import router as ws_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(ws_router)

@app.get("/")
async def root():
    return {"message": "Сервер успешно запущен!"}
