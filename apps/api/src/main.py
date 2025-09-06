from fastapi import FastAPI, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError

from .config import settings
from .database import Base, engine, get_session
from .routers import auth, tasks, reports, inventory
from .routers import access as access_router
from .routers import handover as handover_router
from .routers import users as users_router
from .models import User

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/api/v1/auth/me")
async def auth_me(authorization: str | None = Header(default=None), db: AsyncSession = Depends(get_session)):
    if not authorization or not authorization.startswith("Bearer "):
        return {"detail": "Not authenticated"}
    token = authorization.split()[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = int(payload.get("sub"))
    except JWTError:
        return {"detail": "Invalid token"}
    res = await db.execute(select(User).where(User.id == user_id))
    user = res.scalar_one_or_none()
    if not user:
        return {"detail": "User not found"}
    return {"id": user.id, "login": user.login, "phone": user.phone, "role": user.role.value, "crew_topic_id": user.crew_topic_id}

app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(tasks.router, prefix=settings.API_V1_PREFIX)
app.include_router(reports.router, prefix=settings.API_V1_PREFIX)
app.include_router(inventory.router, prefix=settings.API_V1_PREFIX)
app.include_router(access_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(handover_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(users_router.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
async def root():
    return {"ok": True, "name": settings.APP_NAME}
