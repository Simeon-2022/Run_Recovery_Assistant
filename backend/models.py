from pydantic import BaseModel, Field
from typing import Literal


class AnalyzeRequest(BaseModel):
    duration: int = Field(..., ge=1, le=600, description="Workout duration in minutes")
    intensity: Literal["low", "medium", "high"]


class FoodItem(BaseModel):
    name: str
    category: Literal["carbs", "protein", "antioxidants"]
    description: str
    nutrients_summary: str


class AnalyzeResponse(BaseModel):
    workout_class: Literal["Light", "Moderate", "Hard"]
    foods: dict[str, list[FoodItem]]
