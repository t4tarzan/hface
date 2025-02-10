from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import os

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers after app initialization
from app.api import auth, tools, admin, memberships

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(tools.router, prefix="/api/tools", tags=["tools"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(memberships.router, prefix="/api/memberships", tags=["memberships"])

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Create handler for AWS Lambda / Vercel
handler = Mangum(app)
