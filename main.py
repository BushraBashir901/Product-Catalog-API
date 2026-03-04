from fastapi import FastAPI
from app.cache import init_cache  
from app.middleware import LoggingMiddleware
from app.api.routes import products, categories, auth

app = FastAPI(
    title="Product Catalog API",
    description="A RESTful API built with FastAPI that provides user signup, login, and JWT-based authentication.",
    openapi_tags=[
        {"name": "Products", "description": "Operations with products"},
        {"name": "Categories", "description": "Operations with categories"},
        {"name": "Auth", "description": "Register, login and manage tokens"}
    ]
)


# Cache initialization
@app.on_event("startup")
async def startup_event():
    init_cache()  

# Middleware
app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(auth.router)