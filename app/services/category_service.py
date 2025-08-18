from app.database import db
from bson import ObjectId

category_collection = db["categories"]

async def create_category(category: dict):
    result = await category_collection.insert_one(category)
    return str(result.inserted_id)

async def list_categories():
    categories = []
    async for category in category_collection.find():
        category["_id"] = str(category["_id"])
        categories.append(category)
    return categories

async def get_category(category_id: str):
    category = await category_collection.find_one({"_id": ObjectId(category_id)})
    if category:
        category["_id"] = str(category["_id"])
    return category

async def delete_category(category_id: str):
    result = await category_collection.delete_one({"_id": ObjectId(category_id)})
    return result.deleted_count > 0
