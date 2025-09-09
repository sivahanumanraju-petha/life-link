
from fastapi import APIRouter, HTTPException
from ..models import EmergencyRequestCreate
from ..database import db
from ..utils import blood_compatible
from bson import ObjectId

router = APIRouter(prefix="/requests", tags=["requests"])

@router.post("/", response_model=dict)
async def create_request(payload: EmergencyRequestCreate):
    doc = {
        "needed_blood_type": payload.needed_blood_type,
        "units": payload.units,
        "note": payload.note,
        "created_at": __import__("datetime").datetime.utcnow()
    }
    res = await db.requests.insert_one(doc)

    # Find best matches (simple scoring)
    cursor = db.donors.find({"available": True})
    matches = []
    async for donor in cursor:
        donor_bt = donor.get("blood_type")
        if not blood_compatible(payload.needed_blood_type, donor_bt):
            continue
        # simple: closer is higher score
        matches.append({
            "donor_id": str(donor["_id"]),
            "name": donor["name"],
            "email": donor["email"],
            "phone": donor.get("phone"),
            "blood_type": donor_bt,
        })
    # sort best first
    matches.sort(key=lambda x: 0, reverse=True)
    # Optionally: notify top N donors (email/sms) - left as TODO
    return {"request_id": str(res.inserted_id), "matches": matches[:10]}
