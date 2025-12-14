from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime



class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: Literal["high", "medium", "low"] = "medium"



class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    priority: Optional[Literal["high", "medium", "low"]]


class TaskResponse(TaskBase):
    id: str
    status: str
    created_at: datetime
