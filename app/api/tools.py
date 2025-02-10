from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from typing import List
import huggingface_hub
from datetime import datetime, timedelta

from ..core.deps import get_current_user, get_db
from ..models import Tool, User, ToolUsage
from ..schemas.tool import ToolCreate, ToolResponse, ToolUpdate
from ..services.tool_service import check_tool_status, log_tool_usage

router = APIRouter()

@router.get("/", response_model=List[ToolResponse])
async def list_tools(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all available tools for the user's membership level"""
    tools = db.query(Tool).filter(
        Tool.is_active == True,
        Tool.is_functioning == True
    ).offset(skip).limit(limit).all()
    
    # Filter tools based on user's membership
    return [tool for tool in tools if tool.id in [mt.tool_id for mt in current_user.membership.membership_tools]]

@router.post("/{tool_id}/execute")
async def execute_tool(
    tool_id: int,
    input_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    _: str = Depends(RateLimiter(times=100, hours=24))  # Rate limit per user
):
    """Execute a specific AI tool"""
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool or not tool.is_active or not tool.is_functioning:
        raise HTTPException(status_code=404, detail="Tool not available")
    
    # Check if user has access to this tool
    if tool_id not in [mt.tool_id for mt in current_user.membership.membership_tools]:
        raise HTTPException(status_code=403, detail="No access to this tool")
    
    # Check usage limits
    today = datetime.utcnow().date()
    usage_count = db.query(ToolUsage).filter(
        ToolUsage.user_id == current_user.id,
        ToolUsage.tool_id == tool_id,
        ToolUsage.created_at >= today
    ).count()
    
    if usage_count >= tool.daily_usage_limit:
        raise HTTPException(status_code=429, detail="Daily usage limit exceeded")
    
    try:
        # Execute the model using Hugging Face
        api = huggingface_hub.InferenceApi(tool.huggingface_model)
        result = api(input_data)
        
        # Log usage
        log_tool_usage(db, current_user.id, tool_id)
        
        return {"result": result}
    except Exception as e:
        tool.is_functioning = False
        tool.error_message = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail="Tool execution failed")
