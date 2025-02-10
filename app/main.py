from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import redis.asyncio as redis
from datetime import datetime
import os

from .core.config import settings
from .api import auth, tools, admin, memberships
from .db.session import engine
from .db import models

app = FastAPI(title="AI Tools Platform")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # Initialize rate limiter
    redis_instance = redis.from_url(os.getenv("REDIS_URL", "redis://localhost"))
    await FastAPILimiter.init(redis_instance)
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tools.router, prefix="/api/tools", tags=["tools"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(memberships.router, prefix="/api/memberships", tags=["memberships"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI Tools Platform"}
