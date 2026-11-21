import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import config
from backend.database import db_store
from backend.routes import (
    destinations,
    states,
    hidden_gems,
    food,
    festivals,
    trip_planner,
    budget,
    transport,
    auth
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("travelmatene.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing TravelMateNE Backend Engine...")
    if config.MONGODB_URI:
        db_store.connect_mongo(config.MONGODB_URI, config.DATABASE_NAME)
    else:
        logger.info("Operating in standalone high-performance JSON data mode.")
    yield
    logger.info("Shutting down TravelMateNE Backend.")

app = FastAPI(
    title="TravelMateNE API — Explore Northeast India",
    description="Official REST APIs powering the TravelMateNE travel discovery, AI trip planner, and culture explorer.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(destinations.router)
app.include_router(states.router)
app.include_router(hidden_gems.router)
app.include_router(food.router)
app.include_router(festivals.router)
app.include_router(trip_planner.router)
app.include_router(budget.router)
app.include_router(transport.router)
app.include_router(auth.router)

@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "TravelMateNE API",
        "database_mode": "MongoDB Atlas" if db_store.is_mongo_connected else "Local High-Performance JSON Store",
        "gemini_ai_configured": bool(config.GEMINI_API_KEY),
        "destinations_count": len(db_store.get_destinations()),
        "states_count": len(db_store.get_states()),
        "hidden_gems_count": len(db_store.get_hidden_gems()),
        "food_count": len(db_store.get_food()),
        "festivals_count": len(db_store.get_festivals())
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=config.HOST, port=config.PORT, reload=True)
