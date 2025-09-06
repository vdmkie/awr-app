from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.hash import bcrypt

from ..database import get_session
from ..models import User, Role
from ..schemas import UserOut
from ..deps import role_required

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_session), _=Depends(role_required([Role.super_admin, Role.admin]))):
    res = await db.execute(select(User))
    return res.scalars().all()

@router.post("/", response_model=UserOut)
async def create_user(login: str, password: str, phone: str | None = None, role: Role = Role.crew, crew_topic_id: str | None = None, db: AsyncSession = Depends(get_session), _=Depends(role_required([Role.super_admin, Role.admin]))):
    res = await db.execute(select(User).where(User.login == login))
    if res.scalar_one_or_none():
        raise HTTPException(400, "Login already exists")
    u = User(
        login=login,
        password_hash=bcrypt.hash(password),
        phone=phone,
        role=role,
        crew_topic_id=crew_topic_id
    )
    db.add(u)
    await db.commit(); await db.refresh(u)
    return u

@router.patch("/{user_id}", response_model=UserOut)
async def update_user(user_id: int, phone: str | None = None, role: Role | None = None, crew_topic_id: str | None = None, password: str | None = None, db: AsyncSession = Depends(get_session), _=Depends(role_required([Role.super_admin, Role.admin]))):
    u = await db.get(User, user_id)
    if not u:
        raise HTTPException(404, "User not found")
    if phone is not None:
        u.phone = phone
    if role is not None:
        u.role = role
    if crew_topic_id is not None:
        u.crew_topic_id = crew_topic_id
    if password is not None:
        u.password_hash = bcrypt.hash(password)
    await db.commit(); await db.refresh(u)
    return u

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session), _=Depends(role_required([Role.super_admin, Role.admin]))):
    u = await db.get(User, user_id)
    if not u:
        raise HTTPException(404, "User not found")
    await db.delete(u)
    await db.commit()
    return {"ok": True}

@router.post("/{user_id}/reset_password")
async def reset_password(user_id: int, db: AsyncSession = Depends(get_session), _=Depends(role_required([Role.super_admin, Role.admin]))):
    u = await db.get(User, user_id)
    if not u:
        raise HTTPException(404, "User not found")
    u.password_hash = bcrypt.hash("1")
    await db.commit()
    return {"ok": True, "new_password": "1"}
