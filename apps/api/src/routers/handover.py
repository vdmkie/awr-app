from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_session
from ..models import HandoverHouse

router = APIRouter(prefix="/handover", tags=["handover"])

@router.get("/")
async def list_houses(db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(HandoverHouse).order_by(HandoverHouse.created_at.desc()))
    return [{"id": h.id, "address": h.address, "note": h.note} for h in res.scalars().all()]

@router.post("/")
async def create_house(payload: dict, db: AsyncSession = Depends(get_session)):
    h = HandoverHouse(address=payload.get("address"), note=payload.get("note"))
    db.add(h); await db.commit(); await db.refresh(h)
    return {"ok": True, "id": h.id}
