from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db

router = APIRouter()

@router.post("/movies/", response_model=Product)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.create_product(product)

@router.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    db_product = await service.get_product(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.get("/products/", response_model=list[Product])
async def read_products(db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.get_all_products()

@router.delete("/products/{product_id}", response_model=Product)
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    db_product = await service.delete_product(product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
