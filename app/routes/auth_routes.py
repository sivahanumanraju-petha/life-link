from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from bson import ObjectId

from ..models import UserCreate, UserOut
from ..database import db
from auth import hash_password, verify_password, create_access_token
from ..config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ========================
# Register
# ========================
@router.post("/register", response_model=UserOut)
async def register(user: UserCreate):
    # Check if user exists
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password and save
    hashed_pw = hash_password(user.password)
    user_doc = {
        "name": user.name,
        "email": user.email,
        "password": hashed_pw,
    }
    res = await db.users.insert_one(user_doc)

    return UserOut(
        id=str(res.inserted_id),
        name=user.name,
        email=user.email
    )

# ========================
# Login
# ========================
@router.post("/login")
async def login(user: UserCreate):
    # Find user
    db_user = await db.users.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data={"user_id": str(db_user["_id"]), "email": db_user["email"]},
        expires_delta=access_token_expires
    )

    return {"access_token": token, "token_type": "bearer"}
