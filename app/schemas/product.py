from pydantic import BaseModel
from typing import Optional
from datetime import datetime


#REQUEST SCHEMA
#All comman fields are in Base schema 
class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price: float
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    
class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None  

    class Config:
        from_attributes = True  # Pydantic v2 uses this instead of orm_mode
        
#RESPONSE SCHEMA 
class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }
    
class ProductResponse(BaseModel):
    source: str
    data: Product