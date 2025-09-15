from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import recipes_collection
from typing import List
import requests #to call the external Api

app = FastAPI()

MEALDB_API = "https://www.themealdb.com/api/json/v1/1"

class Recipe(BaseModel):
  recipe_name: str
  ingredient_lists: List[str]
  instructions: str
  user_notes: str


#Fetch recipes using ingredient (from TheMealDB API)
@app.get("/recipes/{ingredient}") 
def get_recipes(ingredient: str):
    url = f"{MEALDB_API}/filter.php?i={ingredient}"
    result = requests.get(url)

    if result:
        return{"message": "successful"}
        raise HTTPException(status_code=500, detail="Error fetching data from MealDB")

    data = result.json()

    if not data["meals"]:
        raise HTTPException(status_code=404, detail="No recipes found for that ingredient")

    return {"ingredient": ingredient, "recipes": data["meals"]}

#use post to save a recipe (with user notes) to MongoDB.

@app.post("/recipes/favorites")
def save_favorite(recipe: Recipe):
    recipe_data = recipe.model_dump()
    result = recipes_collection.insert_one(recipe_data)
    return {
        "message": "Recipe saved successfully!","id": str(result.inserted_id),  "saved_recipe": recipe_data
    }

#get all list OF saved favorite recipes from MongoDB.
@app.get("/recipes/favorites")
def list_favorites():
    recipes = list(recipes_collection.find({}, {"_id": 0})) 
    return {"favorites": recipes}
