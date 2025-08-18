from fastapi import APIRouter, HTTPException, Body
from app.models.expense_model import Expense
from app.services import expense_service

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", summary="Create a new expense")
async def create_expense(expense: Expense):
    expense_id = await expense_service.create_expense(expense)
    return {"id": expense_id, "message": "Expense created successfully"}

@router.get("/", summary="List all expenses")
async def list_expenses():
    return await expense_service.list_expenses()

@router.get("/{expense_id}", summary="Get an expense by ID")
async def get_expense(expense_id: str):
    expense = await expense_service.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.delete("/{expense_id}", summary="Delete an expense by ID")
async def delete_expense(expense_id: str):
    deleted = await expense_service.delete_expense(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "Expense deleted successfully"}

@router.patch("/{expense_id}", summary="Update an expense")
async def patch_expense(expense_id: str, expense: dict = Body(...)):
    updated = await expense_service.update_expense(expense_id, expense)
    if not updated:
        raise HTTPException(status_code=404, detail="Expense not found or no changes made")
    return {"id": expense_id, "message": "Expense updated successfully"}