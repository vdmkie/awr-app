from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_session
from ..models import AccessRecord

router = APIRouter(prefix="/access", tags=["access"])

@router.get("/")
async def list_access(q: str | None = None, db: AsyncSession = Depends(get_session)):
    query = select(AccessRecord)
    if q:
        query = query.where(AccessRecord.address.ilike(f"%{q}%"))
    res = await db.execute(query.order_by(AccessRecord.created_at.desc()))
    return [{"id": r.id, "address": r.address, "info": r.info} for r in res.scalars().all()]

@router.post("/")
async def create_access(payload: dict, db: AsyncSession = Depends(get_session)):
    rec = AccessRecord(address=payload.get("address"), info=payload.get("info"))
    db.add(rec); await db.commit(); await db.refresh(rec)
    return {"ok": True, "id": rec.id}
