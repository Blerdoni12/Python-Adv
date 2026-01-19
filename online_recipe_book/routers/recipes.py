import sqlite3
from typing import List
from models.recipe import Recipe, RecipeCreate
from datebase import get_db_connection
from fastapi import APIRouter, HTTPException

router = APIRouter()

def category_exists(category_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("Select 1 from categories where id = ?", (category_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

@router.get(path="/recipes/", response_model=List[Recipe])
def get_recipes(cuisine: str = None, difficulty: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "Select * From recipes where 1=1"
    params = []

    if cuisine:
        query += " AND cuisine = ?"
        params.append(cuisine)
    if difficulty:
        query += " AND difficulty = ?"
        params.append(difficulty)

    cursor.execute(query, params)
    recipes = cursor.fetchall()
    conn.close()

    return [
        Recipe(
            id=row[0],
            name=row[1],
            description=row[2],
            ingredients=row[3],
            instructions=row[4],
            cuisine=row[5],
            difficulty=row[6],
            category_id=row[7]
        )
        for row in recipes
    ]

@router.post(path="/recipes/", response_model=Recipe)
def create_recipe(recipe: RecipeCreate):
    if not category_exists(recipe.category_id):
        raise HTTPException(status_code=400, detail="Category does not exist")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "insert into recipes (name, description, ingredients, instructions, cuisine, difficulty, category_id) values (?, ?, ?, ?, ?, ?, ?)",
        (
            recipe.name,
            recipe.description,
            recipe.ingredients,
            recipe.instructions,
            recipe.cuisine,
            recipe.difficulty,
            recipe.category_id,
        ),
    )

    conn.commit()
    recipe_id = cursor.lastrowid
    conn.close()

    return Recipe(
        id=recipe_id,
        name=recipe.name,
        description=recipe.description,
        ingredients=recipe.ingredients,
        instructions=recipe.instructions,
        cuisine=recipe.cuisine,
        difficulty=recipe.difficulty,
        category_id=recipe.category_id,
    )
