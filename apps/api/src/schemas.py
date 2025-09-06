from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .models import Role, TaskStatus, Unit

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    login: str
    phone: Optional[str] = None
    role: Role

class UserCreate(UserBase):
    password: str
    tg_id: Optional[str] = None

class UserOut(UserBase):
    id: int
    crew_topic_id: Optional[str] = None
    class Config: orm_mode = True

class TaskBase(BaseModel):
    address: str
    floors: Optional[int]
    entrances: Optional[int]
    work_type: str
    tz: Optional[str]
    access_info: Optional[str]
    note: Optional[str]
    assigned_crew_id: Optional[int]
    status: TaskStatus = TaskStatus.new

class TaskCreate(TaskBase): pass

class TaskOut(TaskBase):
    id: int
    class Config: orm_mode = True

class ReportBase(BaseModel):
    task_id: int
    crew_id: int
    comment: Optional[str]
    access_info: Optional[str]
    photo_url: Optional[str]
    materials_used: Optional[str]

class ReportOut(ReportBase):
    id: int
    created_at: datetime
    updated_at: datetime
    class Config: orm_mode = True

class MaterialIn(BaseModel):
    name: str
    unit: Unit
    qty: float

class MoveMaterial(BaseModel):
    material_id: int
    qty: float
    from_user_id: Optional[int]
    to_user_id: Optional[int]

class ToolIn(BaseModel):
    name: str
    serial: str
    holder_user_id: Optional[int]
