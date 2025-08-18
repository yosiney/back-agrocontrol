from app.database import db
from app.models.expense_model import Expense
from bson import ObjectId
from datetime import datetime

expense_collection = db["expenses"]

# List of accepted formats
ACCEPTED_DATE_FORMATS = [
    "%Y-%m-%d",        # 2025-08-17
    "%Y/%m/%d",        # 2025/08/17
    "%d-%m-%Y",        # 17-08-2025
    "%d/%m/%Y",        # 17/08/2025
    "%Y-%m-%dT%H:%M:%S", # 2025-08-17T15:30:00
]

def parse_date(date_str: str) -> datetime:
    """Try to parse a date string into datetime, fallback to now."""
    for fmt in ACCEPTED_DATE_FORMATS:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Invalid date format. Accepted formats: {ACCEPTED_DATE_FORMATS}")

async def create_expense(expense: Expense):
    expense_dict = expense.dict()

    if isinstance(expense_dict["date"], str):
        expense_dict["date"] = parse_date(expense_dict["date"])

    result = await expense_collection.insert_one(expense_dict)
    return str(result.inserted_id)

async def list_expenses():
    expenses = []
    async for expense in expense_collection.find():
        expense["_id"] = str(expense["_id"])

        if isinstance(expense.get("date"), datetime):
            expense["date"] = expense["date"].strftime("%Y-%m-%d")

        expenses.append(expense)
    return expenses

async def get_expense(expense_id: str):
    expense = await expense_collection.find_one({"_id": ObjectId(expense_id)})
    if expense:
        expense["_id"] = str(expense["_id"])

        if isinstance(expense.get("date"), datetime):
            expense["date"] = expense["date"].strftime("%Y-%m-%d")

    return expense

async def delete_expense(expense_id: str):
    result = await expense_collection.delete_one({"_id": ObjectId(expense_id)})
    return result.deleted_count > 0


async def update_expense(expense_id: str, expense_data: dict):
    if "date" in expense_data and isinstance(expense_data["date"], str):
        expense_data["date"] = parse_date(expense_data["date"])

    result = await expense_collection.update_one(
        {"_id": ObjectId(expense_id)},
        {"$set": expense_data}
    )

    return result.modified_count > 0