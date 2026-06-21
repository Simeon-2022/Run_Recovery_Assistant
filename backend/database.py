import os
from typing import Any

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()

_supabase_client: Client | None = None

SEED_FOODS: list[dict[str, str]] = [
    {"name": "Banana", "category": "carbs", "description": "Easy-to-digest post-run fruit.", "nutrients_summary": "Carbohydrates, potassium"},
    {"name": "Sweet Potato", "category": "carbs", "description": "Complex carbohydrates for glycogen refill.", "nutrients_summary": "Carbohydrates, fiber, vitamin A"},
    {"name": "Oats", "category": "carbs", "description": "Sustained-release carbs for recovery meals.", "nutrients_summary": "Complex carbs, beta-glucan"},
    {"name": "Brown Rice", "category": "carbs", "description": "Staple grain to restore energy reserves.", "nutrients_summary": "Complex carbs, manganese"},
    {"name": "Quinoa", "category": "carbs", "description": "Carb-rich grain with additional protein.", "nutrients_summary": "Carbohydrates, protein, magnesium"},
    {"name": "Whole Grain Pasta", "category": "carbs", "description": "Convenient high-carb recovery base.", "nutrients_summary": "Carbohydrates, fiber"},
    {"name": "Lentils", "category": "protein", "description": "Protein-rich legume for muscle repair.", "nutrients_summary": "Protein, iron, folate"},
    {"name": "Chickpeas", "category": "protein", "description": "Versatile vegan protein source.", "nutrients_summary": "Protein, carbohydrates, fiber"},
    {"name": "Tofu", "category": "protein", "description": "Complete soy protein for post-run meals.", "nutrients_summary": "Protein, calcium, iron"},
    {"name": "Tempeh", "category": "protein", "description": "Fermented soy with dense protein content.", "nutrients_summary": "Protein, probiotics, iron"},
    {"name": "Edamame", "category": "protein", "description": "Whole soybeans ideal for snack recovery.", "nutrients_summary": "Protein, fiber, folate"},
    {"name": "Black Beans", "category": "protein", "description": "Legume option with protein and minerals.", "nutrients_summary": "Protein, magnesium, iron"},
    {"name": "Blueberries", "category": "antioxidants", "description": "Berry known for anti-inflammatory compounds.", "nutrients_summary": "Anthocyanins, vitamin C"},
    {"name": "Strawberries", "category": "antioxidants", "description": "Hydrating fruit with antioxidant vitamin C.", "nutrients_summary": "Vitamin C, polyphenols"},
    {"name": "Cherries", "category": "antioxidants", "description": "Supports reduced muscle soreness after effort.", "nutrients_summary": "Anthocyanins, antioxidants"},
    {"name": "Spinach", "category": "antioxidants", "description": "Leafy green supporting micronutrient recovery.", "nutrients_summary": "Vitamin C, vitamin E, carotenoids"},
    {"name": "Kale", "category": "antioxidants", "description": "Nutrient-dense green for recovery bowls.", "nutrients_summary": "Vitamins A, C, K, flavonoids"},
    {"name": "Beetroot", "category": "antioxidants", "description": "Nitrate-rich root with antioxidant activity.", "nutrients_summary": "Betalains, nitrates, folate"},
    # Fats
    {"name": "Avocado", "category": "fats", "description": "Creamy fruit rich in heart-healthy monounsaturated fats.", "nutrients_summary": "Monounsaturated fats, fiber, potassium"},
    {"name": "Almonds", "category": "fats", "description": "Nutrient-dense nut with healthy fats and vitamin E.", "nutrients_summary": "Monounsaturated fats, vitamin E, magnesium"},
    {"name": "Walnuts", "category": "fats", "description": "Omega-3 rich nut supporting anti-inflammatory recovery.", "nutrients_summary": "Omega-3, polyphenols, protein"},
    {"name": "Chia Seeds", "category": "fats", "description": "Tiny seeds packed with omega-3 and fiber.", "nutrients_summary": "Omega-3, fiber, calcium"},
    {"name": "Flaxseeds", "category": "fats", "description": "Plant-based omega-3 source for post-run recovery.", "nutrients_summary": "Omega-3, fiber, lignans"},
    {"name": "Hemp Seeds", "category": "fats", "description": "Complete protein and fat source from hemp.", "nutrients_summary": "Omega-3, omega-6, complete protein"},
    # New PDF-sourced foods
    {"name": "Apple", "category": "carbs", "description": "Whole fruit providing natural sugars and fiber for glycogen restoration.", "nutrients_summary": "Carbohydrates, fiber, vitamin C"},
    {"name": "Orange", "category": "carbs", "description": "Citrus fruit rich in natural carbohydrates and immune-supporting vitamin C.", "nutrients_summary": "Carbohydrates, vitamin C, folate"},
    {"name": "Mango", "category": "carbs", "description": "Tropical fruit delivering natural sugars for rapid glycogen replenishment.", "nutrients_summary": "Carbohydrates, vitamins A and C"},
    {"name": "Red Kidney Beans", "category": "protein", "description": "Hearty legume supplying complete protein for muscle repair.", "nutrients_summary": "Protein, iron, folate"},
    {"name": "Green Peas", "category": "protein", "description": "Mild legume rich in plant protein and essential vitamins.", "nutrients_summary": "Protein, vitamins C and K, fiber"},
    {"name": "Split Peas", "category": "protein", "description": "Cooked split peas providing sustained protein and complex carbs.", "nutrients_summary": "Protein, fiber, iron"},
    {"name": "Romaine Lettuce", "category": "antioxidants", "description": "Crisp leafy green with hydrating and antioxidant properties.", "nutrients_summary": "Vitamins A, C, K, folate"},
    {"name": "Cucumber", "category": "antioxidants", "description": "Hydrating vegetable with anti-inflammatory compounds.", "nutrients_summary": "Vitamin K, potassium, antioxidants"},
    {"name": "Cashews", "category": "fats", "description": "Creamy nut providing healthy fats and recovery minerals.", "nutrients_summary": "Monounsaturated fats, magnesium, zinc"},
    {"name": "Pistachios", "category": "fats", "description": "Nutrient-dense nut with antioxidants and heart-healthy fats.", "nutrients_summary": "Monounsaturated fats, vitamin B6, potassium"},
]


def get_supabase_client() -> Client:
    global _supabase_client

    if _supabase_client is not None:
        return _supabase_client

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_KEY must be set. "
            "Copy backend/.env.example to backend/.env and fill values."
        )

    _supabase_client = create_client(supabase_url, supabase_key)
    return _supabase_client


def seed_foods_if_empty() -> None:
    client = get_supabase_client()
    response = client.table("foods").select("id", count="exact").limit(1).execute()

    if response.count and response.count > 0:
        return

    client.table("foods").insert(SEED_FOODS).execute()


def seed_fat_foods_if_missing() -> None:
    client = get_supabase_client()
    response = client.table("foods").select("id", count="exact").eq("category", "fats").limit(1).execute()
    if response.count and response.count > 0:
        return
    fat_foods = [f for f in SEED_FOODS if f["category"] == "fats"]
    if fat_foods:
        client.table("foods").insert(fat_foods).execute()


def seed_pdf_foods_if_missing() -> None:
    """Insert foods sourced from the PDF reference list if they are not yet in the DB."""
    client = get_supabase_client()
    pdf_food_names = [
        "Apple", "Orange", "Mango",
        "Red Kidney Beans", "Green Peas", "Split Peas",
        "Romaine Lettuce", "Cucumber",
        "Cashews", "Pistachios",
    ]
    existing = client.table("foods").select("name").in_("name", pdf_food_names).execute()
    existing_names = {row["name"] for row in (existing.data or [])}
    to_insert = [
        f for f in SEED_FOODS
        if f["name"] in pdf_food_names and f["name"] not in existing_names
    ]
    if to_insert:
        client.table("foods").insert(to_insert).execute()


# Per-100 g calorie values used to back-fill the DB column (USDA / PDF sources)
_CALORIES_PER_100G: dict[str, int] = {
    "Banana": 89, "Sweet Potato": 86, "Oats": 379, "Brown Rice": 130,
    "Quinoa": 111, "Whole Grain Pasta": 120, "Apple": 52, "Orange": 47,
    "Mango": 60, "Lentils": 116, "Chickpeas": 164, "Tofu": 90,
    "Tempeh": 200, "Edamame": 90, "Black Beans": 132,
    "Red Kidney Beans": 127, "Green Peas": 83, "Split Peas": 117,
    "Blueberries": 57, "Strawberries": 32, "Cherries": 50,
    "Spinach": 23, "Kale": 35, "Beetroot": 43,
    "Romaine Lettuce": 17, "Cucumber": 15,
    "Avocado": 160, "Almonds": 579, "Walnuts": 654,
    "Chia Seeds": 486, "Flaxseeds": 534, "Hemp Seeds": 553,
    "Cashews": 553, "Pistachios": 562,
}


def populate_calorie_columns() -> None:
    """
    Write calories_per_100g into every food row.
    Safe to call before the column exists — any DB error is silently ignored.
    Run migration_add_calories.sql in the Supabase SQL Editor first.
    """
    client = get_supabase_client()
    try:
        for name, cal in _CALORIES_PER_100G.items():
            client.table("foods").update({"calories_per_100g": cal}).eq("name", name).execute()
    except Exception:
        pass  # Column not yet added — run migration_add_calories.sql first


def get_foods_by_category(category: str, limit: int, offset: int = 0) -> list[dict[str, Any]]:
    client = get_supabase_client()
    response = (
        client.table("foods")
        .select("*")
        .eq("category", category)
        .range(offset, offset + limit - 1)
        .execute()
    )
    return response.data or []
