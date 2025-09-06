from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from jose import jwt

from ..config import settings
from ..database import get_session
from ..models import User, Role
from ..schemas import Token, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/seed", response_model=list[UserOut])
async def seed(db: AsyncSession = Depends(get_session)):
    demo = [
        ("sa", Role.super_admin),
        ("a1", Role.admin),
        ("b1", Role.crew),
        ("b2", Role.crew),
        ("sk1", Role.storekeeper),
    ]
    created = []
    for login, role in demo:
        res = await db.execute(select(User).where(User.login == login))
        if not res.scalar_one_or_none():
            u = User(login=login, password_hash=bcrypt.hash("1"), role=role)
            db.add(u)
            created.append(u)
    await db.commit()
    return created

@router.post("/register", response_model=UserOut)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(User).where((User.login == payload.login)))
    if res.scalar_one_or_none():
        raise HTTPException(400, "Login already exists")
    u = User(
        login=payload.login,
        password_hash=bcrypt.hash(payload.password),
        tg_id=payload.tg_id,
        role=payload.role,
        phone=payload.phone,
    )
    db.add(u)
    await db.commit()
    await db.refresh(u)
    return u

@router.post("/token", response_model=Token)
async def token(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(User).where(User.login == form.username))
    user = res.scalar_one_or_none()
    if not user or not bcrypt.verify(form.password, user.password_hash):
        raise HTTPException(401, "Incorrect login or password")
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user.id), "exp": expire}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def me(db: AsyncSession = Depends(get_session), form: OAuth2PasswordRequestForm | None = None, token: str | None = None):
    # Simple endpoint if Authorization header set; else not used in this stub
    return {"login": "me", "phone": None, "role": Role.admin, "id": 0, "crew_topic_id": None}

@router.post("/tg_login", response_model=Token)
async def tg_login(tg_id: str, db: AsyncSession = Depends(get_session)):
    res = await db.execute(select(User).where(User.tg_id == tg_id))
    user = res.scalar_one_or_none()
    if not user:
        raise HTTPException(401, "Telegram ID not found")
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user.id), "exp": expire}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}
