from pydantic import BaseModel, Field

class BrutHashRequest(BaseModel):
    hash: str = Field(..., description="Хеш RAR-архива")
    charset: str = Field(..., description="Словарь символов для генерации паролей")
    max_length: int = Field(..., ge=1, le=8, description="Максимальная длина пароля")

class BrutHashResponse(BaseModel):
    task_id: str

class TaskStatusResponse(BaseModel):
    status: str
    progress: int
    result: str | None
