from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Creator of category that just stored
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationships ->ORM
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")
    user = relationship("User", back_populates="categories")