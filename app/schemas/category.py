from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime

#REQUEST SCHEMAS
#All comman fields are in Base schema
class CategoryBase(BaseModel):
    name: str
    description: Optional[str]
    
class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str]=None
    description: Optional[str]=None


#RESPONSE SCHEMA
class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }
    
class CategoryListResponse(BaseModel):
    source: str
    data: List[Category]
    
class CategoryResponse(BaseModel):
    source: str
    data: Category