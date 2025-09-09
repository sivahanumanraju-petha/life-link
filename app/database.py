from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URI, DB_NAME

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Access the "users" collection
user_collection = db.users

# Call this on startup to create indexes
async def init_db():
    try:
        # donors collection: 2dsphere index for geo queries
        await db.donors.create_index([("location", "2dsphere")])
        # users collection: unique email index
        await db.users.create_index("email", unique=True)
        print("✅ MongoDB indexes ensured")
    except Exception as e:
        print("❌ Error creating indexes:", e)

    return db
