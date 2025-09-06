from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import httpx

from ..database import get_session
from ..models import Report, Task, TaskStatus, User
from ..schemas import ReportBase, ReportOut
from ..config import settings

router = APIRouter(prefix="/reports", tags=["reports"])

@router.post("/upsert", response_model=ReportOut)
async def upsert_report(payload: ReportBase, part: int, db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(Report).where(Report.task_id == payload.task_id, Report.crew_id == payload.crew_id))
    r = res.scalar_one_or_none()
    if not r:
        r = Report(task_id=payload.task_id, crew_id=payload.crew_id)
        db.add(r)
    if part == 1 and payload.comment is not None:
        r.comment = payload.comment; r.has_comment = True
    if part == 2 and payload.access_info is not None:
        r.access_info = payload.access_info; r.has_access = True
    if part == 3 and payload.photo_url is not None:
        r.photo_url = payload.photo_url; r.has_photo = True
    if part == 4 and payload.materials_used is not None:
        r.materials_used = payload.materials_used; r.has_materials = True

    r.updated_at = datetime.utcnow()
    await db.commit(); await db.refresh(r)

    t = await db.get(Task, payload.task_id)
    if t and all([r.has_comment, r.has_access, r.has_photo, r.has_materials]) and t.status == TaskStatus.in_progress:
        t.status = TaskStatus.done
        await db.commit()

    return r

@router.get("/", response_model=list[ReportOut])
async def list_reports(task_id: int | None = None, crew_id: int | None = None, db: AsyncSession = Depends(get_session)):
    q = select(Report)
    if task_id:
        q = q.where(Report.task_id == task_id)
    if crew_id:
        q = q.where(Report.crew_id == crew_id)
    res = await db.execute(q.order_by(Report.created_at.desc()))
    return res.scalars().all()
