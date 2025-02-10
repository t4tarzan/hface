from sqlalchemy.orm import Session
import huggingface_hub
from datetime import datetime, timedelta
import asyncio
from typing import List

from ..models import Tool
from ..db.session import SessionLocal

async def check_tool_status(tool: Tool, db: Session) -> bool:
    """Check if a tool is functioning by testing it with sample data"""
    try:
        api = huggingface_hub.InferenceApi(tool.huggingface_model)
        
        # Use appropriate sample data based on tool category
        sample_data = get_sample_data(tool.category)
        _ = api(sample_data)
        
        tool.is_functioning = True
        tool.error_message = None
        tool.last_status_check = datetime.utcnow()
        db.commit()
        return True
    except Exception as e:
        tool.is_functioning = False
        tool.error_message = str(e)
        tool.last_status_check = datetime.utcnow()
        db.commit()
        return False

def get_sample_data(category: str) -> dict:
    """Get appropriate sample data for testing based on tool category"""
    samples = {
        "text": {"inputs": "Hello, world!"},
        "image": {"inputs": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"},
        "audio": {"inputs": "Hello"},
        "video": {"inputs": "Hello"},
        "other": {"inputs": "test"}
    }
    return samples.get(category, samples["other"])

async def monitor_tools():
    """Periodic task to monitor all active tools"""
    while True:
        db = SessionLocal()
        try:
            tools = db.query(Tool).filter(Tool.is_active == True).all()
            for tool in tools:
                # Check tools that haven't been checked in the last hour
                if (not tool.last_status_check or 
                    datetime.utcnow() - tool.last_status_check > timedelta(hours=1)):
                    await check_tool_status(tool, db)
        finally:
            db.close()
        
        # Wait for 1 hour before next check
        await asyncio.sleep(3600)

def start_monitoring():
    """Start the tool monitoring process"""
    loop = asyncio.get_event_loop()
    loop.create_task(monitor_tools())
