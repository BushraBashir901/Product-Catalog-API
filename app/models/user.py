from sqlalchemy import Column,String,Integer,DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    categories = relationship("Category", back_populates="user")  # One-to-Many
    products = relationship("Product", back_populates="user")     # One-to-Many