from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NoteResponse(BaseModel):
    id: int
    email: str
    title: str
    content: str
    filename: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
