import re

from fastapi import APIRouter

from database import get_foods_by_category
from logic import classify_workout, get_food_counts, get_macro_allocation, get_meal_plan_counts
from models import AnalyzeRequest, AnalyzeResponse, FoodItem, MacroAllocation, MealFood, MealItem

router = APIRouter(prefix="/api", tags=["recovery"])


FOOD_SERVING_SIZES: dict[str, str] = {
    "Banana":            "200 g",
    "Sweet Potato":      "250 g cooked",
    "Oats":              "80 g dry",
    "Brown Rice":        "220 g cooked",
    "Quinoa":            "200 g cooked",
    "Whole Grain Pasta": "220 g cooked",
    "Apple":             "100 g",
    "Orange":            "100 g",
    "Mango":             "100 g",
    "Lentils":           "198 g cooked",
    "Chickpeas":         "164 g cooked",
    "Tofu":              "180 g",
    "Tempeh":            "160 g",
    "Edamame":           "220 g",
    "Black Beans":       "172 g cooked",
    "Red Kidney Beans":  "100 g cooked",
    "Green Peas":        "100 g cooked",
    "Split Peas":        "100 g cooked",
    "Blueberries":       "180 g",
    "Strawberries":      "220 g",
    "Cherries":          "180 g",
    "Spinach":           "30 g (1 cup)",
    "Kale":              "120 g",
    "Beetroot":          "200 g",
    "Romaine Lettuce":   "100 g",
    "Cucumber":          "100 g",
    "Avocado":           "50 g",
    "Almonds":           "35 g (~23 nuts)",
    "Walnuts":           "30 g (~14 halves)",
    "Chia Seeds":        "20 g",
    "Flaxseeds":         "20 g",
    "Hemp Seeds":        "25 g",
    "Cashews":           "28 g (~18 kernels)",
    "Pistachios":        "28 g (~49 kernels)",
}

# Calories per serving (USDA / Harvard / PDF reference list)
FOOD_CALORIES: dict[str, int] = {
    "Banana":            178,   # 200 g × 89 kcal/100 g
    "Sweet Potato":      215,   # 250 g × 86 kcal/100 g
    "Oats":              303,   # 80 g dry × 379 kcal/100 g
    "Brown Rice":        286,   # 220 g × 130 kcal/100 g cooked
    "Quinoa":            222,   # 200 g × 111 kcal/100 g cooked
    "Whole Grain Pasta": 264,   # 220 g × 120 kcal/100 g cooked
    "Apple":             52,    # 100 g (PDF)
    "Orange":            47,    # 100 g (PDF)
    "Mango":             60,    # 100 g (PDF)
    "Lentils":           230,   # 198 g cooked cup (PDF)
    "Chickpeas":         269,   # 164 g cooked cup (PDF)
    "Tofu":              162,   # 180 g × 90 kcal/100 g
    "Tempeh":            320,   # 160 g × 200 kcal/100 g
    "Edamame":           198,   # 220 g × 90 kcal/100 g
    "Black Beans":       227,   # 172 g cooked cup (PDF)
    "Red Kidney Beans":  127,   # 100 g cooked (PDF)
    "Green Peas":        83,    # 100 g cooked (PDF)
    "Split Peas":        117,   # 100 g cooked (PDF)
    "Blueberries":       102,   # 180 g × 57 kcal/100 g (PDF)
    "Strawberries":      70,    # 220 g × 32 kcal/100 g (PDF)
    "Cherries":          90,    # 180 g × ~50 kcal/100 g
    "Spinach":           7,     # 30 g (PDF)
    "Kale":              42,    # 120 g × 35 kcal/100 g (PDF)
    "Beetroot":          86,    # 200 g × 43 kcal/100 g
    "Romaine Lettuce":   17,    # 100 g (PDF)
    "Cucumber":          15,    # 100 g (PDF)
    "Avocado":           80,    # 50 g × 160 kcal/100 g
    "Almonds":           206,   # 35 g × 165 kcal/28 g (PDF)
    "Walnuts":           204,   # 30 g × 190 kcal/28 g (PDF)
    "Chia Seeds":        97,    # 20 g × 486 kcal/100 g
    "Flaxseeds":         107,   # 20 g × 534 kcal/100 g
    "Hemp Seeds":        138,   # 25 g × 553 kcal/100 g
    "Cashews":           190,   # 28 g (PDF)
    "Pistachios":        160,   # 28 g (PDF)
}


def get_serving_size(food_name: str) -> str:
    return FOOD_SERVING_SIZES.get(food_name, "100 g")


def get_calories(food_name: str) -> int:
    return FOOD_CALORIES.get(food_name, 0)


# Calories per 100 g — USDA / PDF reference values
FOOD_CALORIES_PER_100G: dict[str, int] = {
    "Banana":            89,
    "Sweet Potato":      86,   # cooked
    "Oats":              379,  # dry
    "Brown Rice":        130,  # cooked
    "Quinoa":            111,  # cooked
    "Whole Grain Pasta": 120,  # cooked
    "Apple":             52,
    "Orange":            47,
    "Mango":             60,
    "Lentils":           116,  # cooked
    "Chickpeas":         164,  # cooked
    "Tofu":              90,
    "Tempeh":            200,
    "Edamame":           90,   # cooked
    "Black Beans":       132,  # cooked
    "Red Kidney Beans":  127,  # cooked
    "Green Peas":        83,   # cooked
    "Split Peas":        117,  # cooked
    "Blueberries":       57,
    "Strawberries":      32,
    "Cherries":          50,
    "Spinach":           23,
    "Kale":              35,
    "Beetroot":          43,
    "Romaine Lettuce":   17,
    "Cucumber":          15,
    "Avocado":           160,
    "Almonds":           579,
    "Walnuts":           654,
    "Chia Seeds":        486,
    "Flaxseeds":         534,
    "Hemp Seeds":        553,
    "Cashews":           553,
    "Pistachios":        562,
}


def get_calories_per_100g(food_name: str) -> int:
    return FOOD_CALORIES_PER_100G.get(food_name, 0)


def _parse_grams(serving_size: str) -> float:
    """Return the leading gram quantity from a serving-size string, or 0."""
    m = re.match(r'^(\d+(?:\.\d+)?)\s*g', serving_size)
    return float(m.group(1)) if m else 0.0


def _scale_serving(serving_size: str, scale: float) -> str:
    """Multiply the gram quantity in a serving-size string by *scale*."""
    m = re.match(r'^(\d+(?:\.\d+)?)\s*g(.*)', serving_size)
    if not m:
        return serving_size
    new_grams = round(float(m.group(1)) * scale)
    suffix = re.sub(r'\s*\([^)]*\)', '', m.group(2)).rstrip()
    return f"{new_grams} g{(' ' + suffix.strip()) if suffix.strip() else ''}"


def get_meal_macros(meal_counts: dict[str, int]) -> MacroAllocation:
    carbs = int(meal_counts.get("carbs", 0))
    protein = int(meal_counts.get("protein", 0))
    fats = int(meal_counts.get("fats", 0))

    total = carbs + protein + fats
    if total == 0:
        return MacroAllocation(carbs_percent=0, protein_percent=0, fat_percent=0)

    return MacroAllocation(
        carbs_percent=round((carbs / total) * 100),
        protein_percent=round((protein / total) * 100),
        fat_percent=round((fats / total) * 100),
    )


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_run(payload: AnalyzeRequest) -> AnalyzeResponse:
    workout_class, training_load_score = classify_workout(
        payload.duration,
        payload.mileage,
        payload.pace,
        payload.intensity,
        payload.perceived_effort,
    )

    # Overall food recommendations panel
    food_counts = get_food_counts(workout_class)
    foods_by_category: dict[str, list[FoodItem]] = {}
    for category, count in food_counts.items():
        rows = get_foods_by_category(category, count)
        foods_by_category[category] = [
            FoodItem(
                name=row["name"],
                category=row["category"],
                description=row["description"],
                nutrients_summary=row["nutrients_summary"],
                serving_size=get_serving_size(row["name"]),
                calories_per_serving=get_calories(row["name"]),
                calories_per_100g=get_calories_per_100g(row["name"]),
            )
            for row in rows
        ]

    # Meal plan — pre-fetch full pools then distribute without repeating foods
    meal_plan_counts = get_meal_plan_counts(workout_class)
    category_totals: dict[str, int] = {
        cat: sum(int(m.get(cat, 0)) for m in meal_plan_counts)
        for cat in ("carbs", "protein", "antioxidants", "fats")
    }
    category_pools: dict[str, list[dict]] = {
        cat: get_foods_by_category(cat, total)
        for cat, total in category_totals.items()
        if total > 0
    }
    category_cursors: dict[str, int] = {cat: 0 for cat in category_pools}

    # Breakfast 30 %, Lunch 40 %, Dinner 30 %
    meal_shares = [0.30, 0.40, 0.30]
    calorie_target: int = payload.calorie_target

    meal_items: list[MealItem] = []
    for i, meal in enumerate(meal_plan_counts):
        meal_target_cal = round(calorie_target * meal_shares[i])

        # Collect raw rows for this meal
        raw_rows: list[dict] = []
        for cat in ("carbs", "protein", "antioxidants", "fats"):
            count = int(meal.get(cat, 0))
            pool = category_pools.get(cat, [])
            cursor = category_cursors.get(cat, 0)
            raw_rows.extend(pool[cursor: cursor + count])
            category_cursors[cat] = cursor + count

        # Compute serving-size scale so the meal hits its calorie target
        standard_total = sum(get_calories(row["name"]) for row in raw_rows)
        if standard_total > 0:
            raw_scale = meal_target_cal / standard_total
            scale = max(0.5, min(raw_scale, 2.5))  # sensible cap
        else:
            scale = 1.0

        meal_foods: list[MealFood] = []
        for row in raw_rows:
            scaled_cal = round(get_calories(row["name"]) * scale)
            meal_foods.append(
                MealFood(
                    name=row["name"],
                    description=row["description"],
                    nutrients_summary=row["nutrients_summary"],
                    serving_size=_scale_serving(get_serving_size(row["name"]), scale),
                    calories_per_serving=scaled_cal,
                    calories_per_100g=get_calories_per_100g(row["name"]),
                )
            )

        meal_items.append(
            MealItem(
                meal_name=meal["meal_name"],
                foods=meal_foods,
                macros=get_meal_macros(meal),
                meal_calories=sum(f.calories_per_serving for f in meal_foods),
                meal_target=meal_target_cal,
            )
        )

    macro_dict = get_macro_allocation(workout_class)
    macros = MacroAllocation(
        **macro_dict,
        carbs_kcal=round(calorie_target * macro_dict["carbs_percent"] / 100),
        protein_kcal=round(calorie_target * macro_dict["protein_percent"] / 100),
        fat_kcal=round(calorie_target * macro_dict["fat_percent"] / 100),
    )

    return AnalyzeResponse(
        workout_class=workout_class,
        training_load_score=training_load_score,
        foods=foods_by_category,
        meal_plan=meal_items,
        macros=macros,
        calorie_target=calorie_target,
    )


@router.get("/foods")
def list_foods(category: str = "carbs", limit: int = 10) -> list[dict[str, str]]:
    safe_limit = min(max(limit, 1), 50)
    return get_foods_by_category(category, safe_limit)
