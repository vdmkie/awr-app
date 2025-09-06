from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from ..database import get_session
from ..models import Task, TaskStatus, Role
from ..schemas import TaskCreate, TaskOut
from ..deps import role_required

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[TaskOut])
async def list_tasks(status: TaskStatus | None = None, assigned_crew_id: int | None = None, db: AsyncSession = Depends(get_session)):
    q = select(Task)
    if status:
        q = q.where(Task.status == status)
    if assigned_crew_id is not None:
        q = q.where(Task.assigned_crew_id == assigned_crew_id)
    res = await db.execute(q.order_by(Task.created_at.desc()))
    return res.scalars().all()

@router.post("/", response_model=TaskOut)
async def create_task(payload: TaskCreate, db: AsyncSession = Depends(get_session), _=Depends(role_required([Role.super_admin, Role.admin]))):
    t = Task(**payload.model_dump())
    db.add(t); await db.commit(); await db.refresh(t)
    return t

@router.patch("/{task_id}/assign", response_model=TaskOut)
async def assign(task_id: int, crew_id: int, db: AsyncSession = Depends(get_session), _=Depends(role_required([Role.super_admin, Role.admin]))):
    t = await db.get(Task, task_id)
    if not t: raise HTTPException(404, "Task not found")
    t.assigned_crew_id = crew_id
    if t.status == TaskStatus.new:
        t.status = TaskStatus.in_progress
    t.updated_at = datetime.utcnow()
    await db.commit(); await db.refresh(t)
    return t

@router.patch("/{task_id}/status", response_model=TaskOut)
async def set_status(task_id: int, status: TaskStatus, db: AsyncSession = Depends(get_session), _=Depends(role_required([Role.super_admin, Role.admin]))):
    t = await db.get(Task, task_id)
    if not t: raise HTTPException(404, "Task not found")
    t.status = status
    t.updated_at = datetime.utcnow()
    await db.commit(); await db.refresh(t)
    return t
