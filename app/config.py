import os
from dotenv import load_dotenv
load_dotenv()

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://kingshiva6622:Zxcvbnm123@resumestore.e6ihl22.mongodb.net/?retryWrites=true&w=majority&appName=resumestore"
DB_NAME = "lifelink"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

JWT_SECRET = os.getenv("JWT_SECRET", "replace_this_in_prod")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day
