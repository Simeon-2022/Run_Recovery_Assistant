from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import routes
from models import AnalyzeRequest


def _fake_foods() -> dict[str, list[dict[str, str]]]:
    return {
        "carbs": [
            {"name": "Banana", "category": "carbs", "description": "", "nutrients_summary": ""},
            {"name": "Sweet Potato", "category": "carbs", "description": "", "nutrients_summary": ""},
            {"name": "Oats", "category": "carbs", "description": "", "nutrients_summary": ""},
            {"name": "Brown Rice", "category": "carbs", "description": "", "nutrients_summary": ""},
        ],
        "protein": [
            {"name": "Green Peas", "category": "protein", "description": "", "nutrients_summary": ""},
            {"name": "Split Peas", "category": "protein", "description": "", "nutrients_summary": ""},
            {"name": "Lentils", "category": "protein", "description": "", "nutrients_summary": ""},
        ],
        "antioxidants": [
            {"name": "Blueberries", "category": "antioxidants", "description": "", "nutrients_summary": ""},
            {"name": "Strawberries", "category": "antioxidants", "description": "", "nutrients_summary": ""},
            {"name": "Cherries", "category": "antioxidants", "description": "", "nutrients_summary": ""},
        ],
        "fats": [
            {"name": "Avocado", "category": "fats", "description": "", "nutrients_summary": ""},
            {"name": "Almonds", "category": "fats", "description": "", "nutrients_summary": ""},
            {"name": "Walnuts", "category": "fats", "description": "", "nutrients_summary": ""},
        ],
    }


def test_meal_foods_are_in_recovery_food_lists(monkeypatch):
    db = _fake_foods()

    def fake_get_foods_by_category(category: str, limit: int):
        return db[category][:limit]

    monkeypatch.setattr(routes, "get_foods_by_category", fake_get_foods_by_category)

    payload = AnalyzeRequest(
        duration=45,
        mileage=8.5,
        pace=5.29,
        intensity="moderate",
        perceived_effort=3,
        calorie_target=2000,
    )

    response = routes.analyze_run(payload)

    recovery_names = {
        food.name
        for foods in response.foods.values()
        for food in foods
    }
    meal_names = {
        food.name
        for meal in response.meal_plan
        for food in meal.foods
    }

    assert meal_names.issubset(recovery_names)
    assert "Brown Rice" in recovery_names
    assert "Cherries" in recovery_names
    assert "Walnuts" in recovery_names
