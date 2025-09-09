import uvicorn
from fastapi import FastAPI
from app.routes import auth_routes, donor_routes, request_routes
from app.database import init_db

app = FastAPI(title="LifeLink API")

@app.get("/")
async def root():
    return {"message": "LifeLink is running!"}

# Include routers
app.include_router(auth_routes.router)
app.include_router(donor_routes.router)
app.include_router(request_routes.router)

# Startup event → init DB indexes
@app.on_event("startup")
async def startup_event():
    await init_db()

# Run with: python app/main.py
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
