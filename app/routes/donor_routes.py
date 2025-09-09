
import re
from fastapi import APIRouter, HTTPException, Depends, Query
from ..models import DonorCreate, DonorOut
from app.database import db
from bson import ObjectId
from typing import List
from ..utils import haversine_km, blood_compatible

router = APIRouter(prefix="/donors", tags=["donors"])

@router.post("/", response_model=dict)
async def create_donor(payload: DonorCreate):
    doc = {
        "name": payload.name,
        "email": payload.email,
        "phone": payload.phone,
        "blood_type": payload.blood_type,
        "last_donated": payload.last_donated,
        "available": payload.available
    }
    res = await db.donors.insert_one(doc)
    return {"id": str(res.inserted_id)}

@router.get("/search", response_model=List[dict])
async def search_donors(blood_type:str = Query(..., description="e.g. A+, O-, B+")):
    try:
        blood_type = blood_type.strip().upper()
        safe_blood_type = re.escape(blood_type)
        cursor = db.donors.find({
            "blood_type": {"$regex": f"^{safe_blood_type}$", "$options": "i"}
        })

        results = []
        async for doc in cursor:
            results.append({
            "id": str(doc["_id"]),
            "name": doc["name"],
            "email": doc["email"],
            "phone": doc.get("phone"),
            "blood_type": doc["blood_type"],
            "available": doc.get("available")
        })
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
