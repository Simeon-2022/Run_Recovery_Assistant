from fastapi import APIRouter

from database import get_foods_by_category
from logic import classify_workout, get_food_counts
from models import AnalyzeRequest, AnalyzeResponse, FoodItem

router = APIRouter(prefix="/api", tags=["recovery"])


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_run(payload: AnalyzeRequest) -> AnalyzeResponse:
    workout_class = classify_workout(payload.duration, payload.intensity)
    requested_counts = get_food_counts(workout_class)

    foods_by_category: dict[str, list[FoodItem]] = {}
    for category, count in requested_counts.items():
        rows = get_foods_by_category(category, count)
        foods_by_category[category] = [FoodItem(**row) for row in rows]

    return AnalyzeResponse(workout_class=workout_class, foods=foods_by_category)


@router.get("/foods")
def list_foods(category: str = "carbs", limit: int = 10) -> list[dict[str, str]]:
    safe_limit = min(max(limit, 1), 50)
    return get_foods_by_category(category, safe_limit)
