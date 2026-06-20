from pydantic import BaseModel, Field
from typing import Literal


class AnalyzeRequest(BaseModel):
    duration: int = Field(..., ge=1, le=600, description="Workout duration in minutes")
    mileage: float = Field(..., ge=0.1, le=200, description="Distance in kilometres")
    pace: float = Field(..., ge=1.0, le=30.0, description="Pace in minutes per km")
    intensity: Literal["very_low", "low", "moderate", "moderate_high", "high", "very_high"]
    perceived_effort: int = Field(..., ge=1, le=5, description="Perceived effort 1 (very easy) to 5 (maximum)")
    calorie_target: int = Field(2000, ge=800, le=6000, description="Daily calorie target in kcal")


class FoodItem(BaseModel):
    name: str
    category: Literal["carbs", "protein", "antioxidants", "fats"]
    description: str
    nutrients_summary: str
    serving_size: str
    calories_per_serving: int
    calories_per_100g: int


class MealFood(BaseModel):
    name: str
    description: str
    nutrients_summary: str
    serving_size: str
    calories_per_serving: int
    calories_per_100g: int


class MacroAllocation(BaseModel):
    carbs_percent: int
    protein_percent: int
    fat_percent: int
    carbs_kcal: int = 0
    protein_kcal: int = 0
    fat_kcal: int = 0


class MealItem(BaseModel):
    meal_name: str
    foods: list[MealFood]
    macros: MacroAllocation
    meal_calories: int = 0
    meal_target: int = 0


class AnalyzeResponse(BaseModel):
    workout_class: Literal["Light", "Moderate", "Hard"]
    training_load_score: int
    foods: dict[str, list[FoodItem]]
    meal_plan: list[MealItem]
    macros: MacroAllocation
    calorie_target: int = 2000
