
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URI, DB_NAME
from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URI, DB_NAME

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://kingshiva6622:Zxcvbnm123@resumestore.e6ihl22.mongodb.net/?retryWrites=true&w=majority&appName=resumestore"
DB_NAME = "lifelink"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]



# call this on startup to create indexes
async def init_db():
    # donors collection: 2dsphere index for geo queries
    db.donors.create_index([("location", "2dsphere")])
    db.users.create_index("email", unique=True)
