from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from app.schemas.category import Category, CategoryCreate, CategoryUpdate, CategoryListResponse,CategoryResponse
from app.crud import category as crud_category
from app.api.deps import get_db, get_current_user
from app.cache import get_cache, set_cache

router = APIRouter(prefix="/categories", tags=["Categories"])


# Returning list of Categories
@router.get("/", response_model=CategoryListResponse,summary="Returns list of categories",description="Fetches list of categories. Returns cached data if available, otherwise fetches from database.")
def list_categories(db: Session = Depends(get_db)):
    '''
     Retrives all categories from cache and db.
      Returns:
         source: where data came from db,cache
         data:list of categories objects
    Caching:
            if categories exist in cache then it will return from category 
            if category not exsit in cache then it will fetch data from database and cached for 120 sec  
    '''
    cache_key = "category_list"
    cached = get_cache(cache_key)
    if cached:
        return {"source": "cache", "data": cached}

    categories = crud_category.get_categories(db)
    categories_out = [Category.from_orm(c) for c in categories]

    # Use jsonable_encoder to handle datetime serialization
    set_cache(cache_key, jsonable_encoder(categories_out), expire=120)

    return {"source": "db", "data": categories_out}


# Return a single Category
@router.get("/{category_id}", response_model=CategoryResponse,summary="Return a specific Category",description="Return category by providing ID")
def get_category(category_id: int, db: Session = Depends(get_db)):
    '''
    Retrives single category from cache and db.
    Returns:
         source: where data came from db,cache
         data: category objects
    Caching:
            if category exist in cache then it will return from category 
            if category not exist in cache then it will fetch data from database and cached  
    '''
    
    cache_key = f"category:{category_id}"

    cached = get_cache(cache_key)
    if cached:
        return {"source": "cache", "data": cached}

    category = crud_category.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category_out = Category.from_orm(category)
    set_cache(cache_key, jsonable_encoder(category_out), None)

    return {"source": "db", "data": category_out}


# Create Category
@router.post("/", response_model=Category,summary="Create new Category",description="Creating new category by providing data")
def create_category(category: CategoryCreate,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    """
    Create a new category.

    Parameters:
    category: Category data
    db: Database session
    current_user: Authenticated user

    Returns the created category.
    """
    created_category = crud_category.create_category(db, category, current_user.id)
    return Category.from_orm(created_category)


# Update Category
@router.put("/{category_id}", response_model=Category,summary="Update specific Category",description="Updating category by providing ID")
def update_category(category_id: int,updates: CategoryUpdate,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    """
    Update a category by ID.

    Parameters:
    category_id: ID of the category to update
    updates: Fields to update
    db: Database session
    current_user: Authenticated user

    Returns the updated category or 404 if not found.
    """
    db_category = crud_category.update_category(db, category_id, updates)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return Category.from_orm(db_category)


# Delete Category
@router.delete("/{category_id}", response_model=Category,summary="Delete specific Category",description="Deleting category and all its products by providing ID")
def delete_category(category_id: int,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    """
    Delete a category by ID.

    Parameters:
    category_id: ID of the category to Delete
    db: Database session
    current_user: Authenticated user
    Raises:
          HTTPExcetion if category not found 404.

    Returns the deleted category
    """
    db_category = crud_category.delete_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return Category.from_orm(db_category)