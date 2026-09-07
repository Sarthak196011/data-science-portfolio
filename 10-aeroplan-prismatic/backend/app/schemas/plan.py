"""Pydantic Models for Plan & Logistics API"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class Airport(BaseModel):
    id: str
    name: str
    lat: float
    lng: float

class Hub(BaseModel):
    id: str
    name: str
    city: str
    lat: float
    lng: float
    lodging: int
    exp: int

class PlanRequest(BaseModel):
    origin_id: str = Field(..., description="IATA code of origin airport (e.g. JFK)")
    dest_name: str = Field(..., description="Destination name or city")
    travel_class: str = Field("curated", description="Travel tier: economy, curated, first")
    duration_days: int = Field(3, ge=1, le=14, description="Trip duration in days (1-14)")
    lat: Optional[float] = Field(None, description="Destination latitude coordinate")
    lng: Optional[float] = Field(None, description="Destination longitude coordinate")

class FlightLogistics(BaseModel):
    origin_id: str
    destination: str
    distance_km: int
    flight_duration_str: str
    flight_price: int
    non_stop: bool = True

class BudgetFormatted(BaseModel):
    flight_price: str
    lodging_nightly: str
    lodging_total: str
    daily_expenses: str
    total_expenses: str
    flight_and_stay: str
    total_budget: str

class BudgetRaw(BaseModel):
    flight_price: int
    lodging_nightly: int
    lodging_total: int
    daily_expenses: int
    total_expenses: int
    flight_and_stay: int
    total_budget: int

class BudgetMatrix(BaseModel):
    formatted: BudgetFormatted
    raw: BudgetRaw

class DaySchedule(BaseModel):
    morning: str
    afternoon: str
    evening: str

class DayItinerary(BaseModel):
    day: int
    title: str
    theme: str
    locations: List[str]
    schedule: DaySchedule
    culinary: Optional[str] = None

class PlanResponse(BaseModel):
    origin: Dict[str, Any]
    destination: Dict[str, Any]
    travel_class: str
    duration_days: int
    flight_logistics: FlightLogistics
    budget_matrix: BudgetMatrix
    itinerary: List[DayItinerary]

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
