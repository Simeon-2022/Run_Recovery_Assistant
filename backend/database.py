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


def get_foods_by_category(category: str, limit: int) -> list[dict[str, Any]]:
    client = get_supabase_client()
    response = (
        client.table("foods")
        .select("name, category, description, nutrients_summary")
        .eq("category", category)
        .limit(limit)
        .execute()
    )
    return response.data or []
