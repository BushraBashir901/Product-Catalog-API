from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


#Operation for getting all categories
def get_products(db: Session, skip: int = 0, limit: int = 100, category_id: int = None):
    query = db.query(Product)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.offset(skip).limit(limit).all()


#Operation for getting single category
def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


#Operation for creating new category
def create_product(db: Session, product: ProductCreate, user_id: int):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        category_id=product.category_id,
        user_id=user_id
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


#Operation for Updating  existing category
def update_product(db: Session, product_id: int, updates: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None
    for key, value in updates.dict(exclude_unset=True).items():#Update only those fields that re sent by client
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


#Operations for deleting category
def delete_product(db: Session, product_id: int):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None
    db.delete(db_product)
    db.commit()
    return db_product