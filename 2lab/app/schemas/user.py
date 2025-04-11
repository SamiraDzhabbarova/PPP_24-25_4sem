from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    token: str

    model_config = {
        "from_attributes": True
    }

class UserMeResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True
    }
