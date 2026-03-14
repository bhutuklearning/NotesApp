from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.pyobjectid import PyObjectId

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class NoteResponse(NoteBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    owner_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        populate_by_name = True
        json_encoders = {PyObjectId: str}
