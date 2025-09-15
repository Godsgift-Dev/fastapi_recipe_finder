from fastapi import FastAPI
from pydantic import BaseModel
from db import recipes_collection
from typing import List
import requests 


#from dotenv import MEALDB_API

app = FastAPI(title= "Welcome to Godsgift Kitchen", description= "Here, you'll find everything about food")

#MEALDB_API = os.getenv("MEALDB_API")

class Recipe(BaseModel):
  recipe_name: str
  ingredient_lists: List[str]
  instructions: str
  user_notes: str


MEALDB_API = "https://www.themealdb.com/api/json/v1/1"

@app.get("/", tags=["Homepage"])
def get_home():
    return {"message": "You are on the recipe finder page"}



#get recipes using ingredient (from TheMealDB API)
@app.get("/recipes/{ingredient}", tags=["Recipe Finder"]) 
def get_recipes(ingredient: str):
    external_api = f"{MEALDB_API}/filter.php?i={ingredient}"
    response = requests.get(external_api)
    data = response.json()
    if response:
        return {"ingredient": ingredient, "recipes": data["meals"]}
    else:
        return{"message": "Error, ingredient not found"}


#save favourite recipes
@app.post("/recipes/favorites", tags=["Recipe Finder"])
def save_favorite(recipe: Recipe):
    recipe_data = recipe.model_dump()
    result = recipes_collection.insert_one(recipe_data)
    return {"message": "Recipe saved successfully!","id": str(result.ObjectId),  "saved_recipe": recipe_data}


#get all list OF saved favorite recipes from MongoDB.
@app.get("/recipes/favorites", tags=["Recipe Finder"])
def list_favorites():
    recipes = list(recipes_collection.find({}))
    return {"favorites": recipes}
