import re
import numpy as np
from datetime import datetime

# ==========================================
# INGREDIENT DATABASE
# ==========================================

ingredient_db = {
    "rice": {
        "price": 80,
        "calories": 200,
        "protein": 4,
    },

    "chicken": {
        "price": 250,
        "calories": 250,
        "protein": 27,
        "diet": "non-veg",
        "substitute": "tofu"
    },

    "oil": {
        "price": 120,
        "calories": 120,
        "protein": 0,
    },

    "onions": {
        "price": 30,
        "calories": 40,
        "protein": 1,
    }
}

# ==========================================
# PANTRY DATA
# ==========================================

pantry = {
    "rice": 5,
    "oil": 10
}

# ==========================================
# PARSE RECIPE USING REGEX
# ==========================================

def parse_recipe(recipe_text):
    pattern = r'(\d+\.?\d*)\s+(\w+)\s+(.+)'
    ingredients = []

    lines = recipe_text.strip().split("\n")

    for line in lines:
        match = re.match(pattern, line.strip())

        if match:
            quantity = float(match.group(1))
            unit = match.group(2)
            ingredient = match.group(3).lower()

            ingredients.append({
                "ingredient": ingredient,
                "quantity": quantity,
                "unit": unit
            })

    return ingredients

# ==========================================
# SCALE RECIPE
# ==========================================

def scale_recipe(ingredients, original_servings, target_servings):
    factor = target_servings / original_servings

    quantities = np.array([
        item["quantity"] for item in ingredients
    ])

    scaled_quantities = quantities * factor

    for i, item in enumerate(ingredients):
        item["scaled_quantity"] = round(
            scaled_quantities[i], 2
        )

    return ingredients

# ==========================================
# COST + CALORIES + PROTEIN
# ==========================================

def calculate_totals(ingredients):
    total_cost = 0
    total_calories = 0
    total_protein = 0

    for item in ingredients:
        name = item["ingredient"]

        if name in ingredient_db:
            db = ingredient_db[name]
            qty = item["scaled_quantity"]

            cost = qty * db["price"]
            calories = qty * db["calories"]
            protein = qty * db["protein"]

            item["cost"] = round(cost, 2)
            item["calories"] = round(calories, 2)
            item["protein"] = round(protein, 2)

            total_cost += cost
            total_calories += calories
            total_protein += protein

    return (
        round(total_cost, 2),
        round(total_calories, 2),
        round(total_protein, 2)
    )

# ==========================================
# SHOPPING LIST
# ==========================================

def generate_shopping_list(ingredients):
    shopping = []

    for item in ingredients:
        ingredient = item["ingredient"]
        needed = item["scaled_quantity"]
        available = pantry.get(ingredient, 0)

        if available < needed:
            buy_amount = needed - available

            shopping.append(
                f"{buy_amount} {item['unit']} {ingredient}"
            )

    return shopping

# ==========================================
# BUDGET CHECK
# ==========================================

def check_budget(total_cost, budget):
    if total_cost > budget:
        return "OVER BUDGET"

    return "WITHIN BUDGET"

# ==========================================
# MEAL RECOMMENDATION
# ==========================================

def recommend_meal():
    if "rice" in pantry and "oil" in pantry:
        return "Recommended Meal: Fried Rice"

    return "No Recommendation"

# ==========================================
# MAIN PROGRAM
# ==========================================

recipe = """
2 cups rice
1 kg chicken
3 tbsp oil
2 pieces onions
"""

print("\nSMART RECIPE OPTIMIZER")
print("=" * 50)

print("\nORIGINAL RECIPE")
print(recipe)

original_servings = int(
    input("\nRecipe serves how many people? ")
)

target_servings = int(
    input("How many people needed? ")
)

budget = float(
    input("Enter your budget ₹: ")
)

# Parse recipe
ingredients = parse_recipe(recipe)

# Scale recipe
ingredients = scale_recipe(
    ingredients,
    original_servings,
    target_servings
)

# Calculate totals
total_cost, total_calories, total_protein = calculate_totals(
    ingredients
)

# Shopping list
shopping_list = generate_shopping_list(
    ingredients
)

# Budget status
budget_status = check_budget(
    total_cost,
    budget
)

# Meal recommendation
meal = recommend_meal()

# ==========================================
# OUTPUT
# ==========================================

print("\nSCALED RECIPE")
print("=" * 50)

for item in ingredients:
    print(
        f"{item['ingredient']} | "
        f"{item['scaled_quantity']} {item['unit']} | "
        f"₹{item['cost']} | "
        f"{item['calories']} cal | "
        f"{item['protein']}g protein"
    )

print("\nTOTAL SUMMARY")
print("=" * 50)

print("Total Cost: ₹", total_cost)
print("Total Calories:", total_calories)
print("Total Protein:", total_protein, "g")

print("\nBUDGET STATUS")
print("=" * 50)

print(budget_status)

print("\nSHOPPING LIST")
print("=" * 50)

for item in shopping_list:
    print("-", item)

print("\nMEAL RECOMMENDATION")
print("=" * 50)

print(meal)

print("\nGenerated on:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
