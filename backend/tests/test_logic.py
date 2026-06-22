import pytest

from backend import logic


def test_classify_workout_signature_and_return():
    wc, score = logic.classify_workout(duration=30, mileage=5.0, pace=5.5, intensity="moderate", perceived_effort=2)
    assert wc in ("Light", "Moderate", "Hard")
    assert isinstance(score, int)


def test_get_food_counts_and_macros():
    counts = logic.get_food_counts("Moderate")
    macros = logic.get_macro_allocation("Moderate")
    assert counts["carbs"] == 3
    assert macros["carbs_percent"] == 55


def test_meal_plan_structure():
    plan = logic.get_meal_plan_counts("Hard")
    assert isinstance(plan, list)
    assert all("meal_name" in m for m in plan)
