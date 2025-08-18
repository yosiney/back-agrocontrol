from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI, DB_NAME

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

async def test_connection():
    try:
        await db.command("ping")
        print("Connected to MongoDB successfully!")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False
