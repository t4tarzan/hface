from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from ..db.base_class import Base
from datetime import datetime

class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float)
    request_limit = Column(Integer)  # Daily request limit
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship("User", back_populates="membership")
    membership_tools = relationship("MembershipTool", back_populates="membership")

class MembershipTool(Base):
    __tablename__ = "membership_tools"

    id = Column(Integer, primary_key=True, index=True)
    membership_id = Column(Integer, ForeignKey("memberships.id"))
    tool_id = Column(Integer, ForeignKey("tools.id"))
    
    # Relationships
    membership = relationship("Membership", back_populates="membership_tools")
    tool = relationship("Tool", back_populates="membership_tools")
