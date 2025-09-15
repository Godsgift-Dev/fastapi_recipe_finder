from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

#connect to mongo atlas cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))

#Access database
fastapi_recipe_finder_db = mongo_client["recipe_finder_db"]

#pick a connection to operate on
recipes_collection = fastapi_recipe_finder_db["recipes"]