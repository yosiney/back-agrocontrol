from fastapi import APIRouter, HTTPException
from app.models.category_model import Category
from app.services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", summary="Create a new category")
async def create_category(category: Category):
    category_id = await category_service.create_category(category.dict())
    return {"id": category_id, "message": "Category created successfully"}

@router.get("/", summary="List all categories")
async def list_categories():
    return await category_service.list_categories()

@router.get("/{category_id}", summary="Get category by ID")
async def get_category(category_id: str):
    category = await category_service.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.delete("/{category_id}", summary="Delete category")
async def delete_category(category_id: str):
    deleted = await category_service.delete_category(category_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}
