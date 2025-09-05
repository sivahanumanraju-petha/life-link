
from math import radians, cos, sin, asin, sqrt

def haversine_km(lat1, lon1, lat2, lon2):
    # Returns distance in kilometers
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth radius km
    return c * r

def blood_compatible(requested: str, donor: str) -> bool:
    # Simple compatibility (you can expand)
    requested = requested.upper()
    donor = donor.upper()
    if requested == donor:
        return True
    # add more rules as needed (e.g., O- universal donor)
    if donor == "O-":
        return True
    if donor == "O+" and requested.endswith("+"):
        return True
    return False
