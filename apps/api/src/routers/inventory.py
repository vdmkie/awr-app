from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_session
from ..models import Material, Tool, UserMaterial, Unit, Role
from ..schemas import MaterialIn, MoveMaterial, ToolIn
from ..deps import role_required

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.post("/materials/add")
async def add_material(payload: MaterialIn, db: AsyncSession = Depends(get_session), _=Depends(role_required([Role.super_admin, Role.storekeeper, Role.admin]))):
    res = await db.execute(select(Material).where(Material.name == payload.name))
    m = res.scalar_one_or_none()
    if not m:
        m = Material(name=payload.name, unit=payload.unit, total_qty=0)
        db.add(m)
    m.total_qty += payload.qty
    await db.commit()
    return {"ok": True}

@router.post("/materials/move")
async def move_material(payload: MoveMaterial, db: AsyncSession = Depends(get_session), _=Depends(role_required([Role.super_admin, Role.storekeeper, Role.admin]))):
    m = await db.get(Material, payload.material_id)
    if not m:
        raise HTTPException(404, "Material not found")

    async def get_um(user_id: int):
        res = await db.execute(select(UserMaterial).where(UserMaterial.user_id == user_id, UserMaterial.material_id == m.id))
        um = res.scalar_one_or_none()
        if not um:
            um = UserMaterial(user_id=user_id, material_id=m.id, qty=0)
            db.add(um)
        return um

    if payload.from_user_id is None and payload.to_user_id:  # выдача со склада
        if m.total_qty < payload.qty:
            raise HTTPException(400, "Not enough on warehouse")
        m.total_qty -= payload.qty
        to_um = await get_um(payload.to_user_id)
        to_um.qty += payload.qty

    elif payload.from_user_id and payload.to_user_id is None:  # возврат на склад
        from_um = await get_um(payload.from_user_id)
        if from_um.qty < payload.qty:
            raise HTTPException(400, "Not enough on user")
        from_um.qty -= payload.qty
        m.total_qty += payload.qty

    elif payload.from_user_id and payload.to_user_id:  # между бригадами
        from_um = await get_um(payload.from_user_id)
        if from_um.qty < payload.qty:
            raise HTTPException(400, "Not enough on user")
        to_um = await get_um(payload.to_user_id)
        from_um.qty -= payload.qty
        to_um.qty += payload.qty

    else:
        raise HTTPException(400, "Wrong move combination")

    await db.commit()
    return {"ok": True}

@router.post("/tools/add")
async def add_tool(payload: ToolIn, db: AsyncSession = Depends(get_session), _=Depends(role_required([Role.super_admin, Role.storekeeper]))):
    t = Tool(name=payload.name, serial=payload.serial, holder_user_id=payload.holder_user_id)
    db.add(t)
    await db.commit()
    return {"ok": True}

@router.post("/tools/transfer")
async def transfer_tool(serial: str, to_user_id: int | None, db: AsyncSession = Depends(get_session), _=Depends(role_required([Role.super_admin, Role.storekeeper]))):
    res = await db.execute(select(Tool).where(Tool.serial == serial))
    t = res.scalar_one_or_none()
    if not t:
        raise HTTPException(404, "Tool not found")
    t.holder_user_id = to_user_id
    await db.commit()
    return {"ok": True}

@router.get("/warehouse/summary")
async def warehouse_summary(db: AsyncSession = Depends(get_session)):
    mats = (await db.execute(select(Material))).scalars().all()
    tools = (await db.execute(select(Tool))).scalars().all()
    return {
        "materials": [{"id": m.id, "name": m.name, "unit": m.unit.value, "qty": m.total_qty} for m in mats],
        "tools": [{"id": t.id, "name": t.name, "serial": t.serial, "holder_user_id": t.holder_user_id} for t in tools],
    }

@router.get("/export.csv")
async def export_csv(db: AsyncSession = Depends(get_session)):
    mats = (await db.execute(select(Material))).scalars().all()
    tools = (await db.execute(select(Tool))).scalars().all()
    lines = ["type,name,unit_or_serial,qty_or_holder"]
    for m in mats:
        lines.append(f"material,{m.name},{m.unit.value},{m.total_qty}")
    for t in tools:
        lines.append(f"tool,{t.name},{t.serial},{t.holder_user_id or ''}")
    csv = "\n".join(lines)
    return Response(content=csv, media_type="text/csv")
