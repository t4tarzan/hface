from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..db.base_class import Base
import enum
from datetime import datetime

class ToolCategory(enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    OTHER = "other"

class Tool(Base):
    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    huggingface_model = Column(String)
    category = Column(Enum(ToolCategory))
    is_active = Column(Boolean, default=True)
    daily_usage_limit = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_status_check = Column(DateTime)
    is_functioning = Column(Boolean, default=True)
    error_message = Column(String, nullable=True)
    
    # Relationships
    usage_logs = relationship("ToolUsage", back_populates="tool")
    membership_tools = relationship("MembershipTool", back_populates="tool")
