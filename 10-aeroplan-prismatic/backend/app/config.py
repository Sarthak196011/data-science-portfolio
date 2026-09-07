"""Application Configuration Settings"""
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Aeroplan Prismatic"
    API_V1_STR: str = "/api"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Vivid 3D Route & Curated Itinerary Generation Engine"
    CORS_ORIGINS: list[str] = ["*"]

settings = Settings()
