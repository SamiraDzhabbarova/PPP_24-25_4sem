from pydantic import BaseModel, Field

class BrutHashRequest(BaseModel):
    hash: str = Field(..., description="Хеш RAR-архива")
    charset: str = Field(..., description="Словарь символов для генерации паролей")
    max_length: int = Field(..., ge=1, le=8, description="Максимальная длина пароля (максимум 8)")

class BrutHashResponse(BaseModel):
    task_id: str

class TaskStatusResponse(BaseModel):
    status: str  # "running", "completed", "failed"
    progress: int  # Процент выполнения (0-100)
    result: str | None  # Найденный пароль или null
