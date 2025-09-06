from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class Role(str, enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
    crew = "crew"
    storekeeper = "storekeeper"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tg_id = Column(String, unique=True, index=True)
    login = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(Role), nullable=False)
    phone = Column(String, nullable=True)
    crew_topic_id = Column(String, nullable=True)

class TaskStatus(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"
    postponed = "postponed"
    problematic = "problematic"

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    address = Column(String, index=True)
    floors = Column(Integer, nullable=True)
    entrances = Column(Integer, nullable=True)
    work_type = Column(String)
    tz = Column(Text, nullable=True)
    access_info = Column(Text, nullable=True)
    note = Column(Text, nullable=True)
    assigned_crew_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.new)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    assigned_crew = relationship("User")

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    crew_id = Column(Integer, ForeignKey("users.id"))
    comment = Column(Text, nullable=True)
    access_info = Column(Text, nullable=True)
    photo_url = Column(Text, nullable=True)
    materials_used = Column(Text, nullable=True)

    has_comment = Column(Boolean, default=False)
    has_access = Column(Boolean, default=False)
    has_photo = Column(Boolean, default=False)
    has_materials = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Unit(str, enum.Enum):
    m = "m"
    pcs = "pcs"
    kg = "kg"

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    unit = Column(Enum(Unit))
    total_qty = Column(Float, default=0)

class Tool(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    serial = Column(String, unique=True, index=True)
    holder_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

class UserMaterial(Base):
    __tablename__ = "user_materials"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    material_id = Column(Integer, ForeignKey("materials.id"))
    qty = Column(Float, default=0)

class AccessRecord(Base):
    __tablename__ = "access_records"
    id = Column(Integer, primary_key=True)
    address = Column(String, index=True)
    info = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class HandoverHouse(Base):
    __tablename__ = "handover_houses"
    id = Column(Integer, primary_key=True)
    address = Column(String, index=True)
    note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
