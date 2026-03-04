from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


#Operation for getting all categories
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).offset(skip).limit(limit).all()


#Operation for getting single category
def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


#Operation for Creating new category
def create_category(db: Session, category: CategoryCreate, user_id: int):
    db_category = Category(
        name=category.name,
        description=category.description,
        user_id=user_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


#Operation for Updating  existing category
def update_category(db: Session, category_id: int, updates: CategoryUpdate):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None
    for key, value in updates.dict(exclude_unset=True).items(): #Updates fields that actually sent by the client to update
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category


#Operations for deleting category
def delete_category(db: Session, category_id: int):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        return None
    db.delete(db_category)
    db.commit()
    return db_category