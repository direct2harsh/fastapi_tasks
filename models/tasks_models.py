

from pydantic import BaseModel, field_validator
from typing import  Optional, List
from enum import Enum
from uuid import UUID
from datetime import datetime



class Status(str,Enum):
    pending = 'pending'
    completed = 'completed'
    in_progress = 'in_progress'

class CreateTask(BaseModel):
    title:str
    description:Optional[str]
    status:Status

    @field_validator('title')
    def check_price_positive(cls, value):
        if len(value) <= 0 or len(value)>256:
            raise ValueError("Title lenght should be between 4 to 256 characters")
        return value

class UpdateTask(BaseModel):
    id: UUID
    title:str    
    status:Status
    @field_validator('title')
    def check_price_positive(cls, value):
        if len(value) < 3 or len(value)>256:
            raise ValueError("Title lenght should be between 4 to 256 characters")
        return value
    

class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] 
    created_at: datetime 
    updated_at: datetime | None

    class Config:
        from_attributes = True

class PaginatedTasksResponse(BaseModel):
    tasks: List[TaskResponse]
    next_task_id: Optional[UUID]
    next_task_created_at: Optional[datetime]
    has_more: bool 

