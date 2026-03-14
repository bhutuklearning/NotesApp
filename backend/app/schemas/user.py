from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.models.pyobjectid import PyObjectId

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user" # user or admin

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: EmailStr
    role: str

    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
