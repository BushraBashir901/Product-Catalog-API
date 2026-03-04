from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.schemas.product import ProductOut, ProductCreate, ProductUpdate
from app.models.product import Product as ProductModel
from app.cache import get_cache, set_cache
from app.api.deps import get_db, get_current_user
from app.crud import product as crud_product

router = APIRouter(prefix="/products",tags=["Products"])

#Return All Products
@router.get("/", response_model=List[ProductOut], summary="List all products")
def list_products(db: Session = Depends(get_db)):
    '''
    Retrieve a list of all products.

    Parameters:
    db: Database session

    Returns a list of products.
    '''
    cache_key = "all_products"

    cached = get_cache(cache_key)
    if cached:
        return cached 

    products = db.query(ProductModel).all()
    if not products:
        raise HTTPException(status_code=404, detail="No products found")

    products_out = [ProductOut.from_orm(p) for p in products]
    set_cache(cache_key, [p.model_dump() for p in products_out], expire=120)

    return products_out


#Create product
@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Create a new product.

    Parameters:
    product: Product data to create
    db: Database session
    current_user: Authenticated user creating the product

    Returns the created product.
    """
    new_product = ProductModel(
        **product.model_dump(),
        user_id=current_user.id 
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    set_cache("all_products", None, expire=None)

    return ProductOut.model_validate(new_product)


#Update product
@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    """
     Update a product by ID.

     Parameters:
     product_id: ID of the product to update
     updates: Fields to update
     db: Database session
     current_user: Authenticated user

    Returns the updated product or 404 if not found.
    """
    existing_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in product.model_dump(exclude_unset=True).items():
        setattr(existing_product, field, value)

    db.commit()
    db.refresh(existing_product)

    set_cache("all_products", None, expire=None)
    return ProductOut.from_orm(existing_product)


#Get single route
@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific products.

    Parameters:
    product_id:unique id of product
    db: Database session

    Returns a single  product.
    """
    cache_key = f"product_{product_id}"
    cached = get_cache(cache_key)
    if cached:
        return cached

    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product_out = ProductOut.from_orm(product)
    set_cache(cache_key, product_out.model_dump(), expire=None)
    return product_out


#Delete product 
@router.delete("/{product_id}", response_model=ProductOut, summary="Delete specific product", description="Deleting products by providing id.")
def delete_product(product_id: int, db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    '''
    Delete a product by ID.

    Parameters:
    product_id: ID of the product to Delete
    db: Database session
    current_user: Authenticated user
    Raises:
          HTTPExcetion if product not found 404.

    Returns the deleted product
    '''
    db_product = crud_product.delete_product(db, product_id, current_user.id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product