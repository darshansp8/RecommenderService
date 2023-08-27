from pymongo import MongoClient
from flask import Blueprint, request, jsonify
import os
import certifi
import ast
import json
import src
#
# mongo = MongoClient("mongodb+srv://dsakpal38:JjTGobCr91gQieH4@cluster0.bnd3i.mongodb.net/", tlsCAFile=certifi.where())
# db = mongo['chefstudio']
# collection = db['recipes']

mongo = MongoClient(os.environ.get("MONGO_URI"), tlsCAFile=certifi.where())
db = mongo.get_database("chefstudio")
collection = db.get_collection("recipes_90k_cleaned")

getdata = Blueprint('getdata',__name__,)


class RecommendedRecipes(object):

    def __init__(self):
        pass

    def get_recipes_by_id(self, ids):
        print(ids)
        # db = mongo.get_database("chefstudio")
        # collection = db.get_collection("recipes_90k")

        response = collection.find({"RecipeId": {"$in": ids}})
        recipe_details = []
        for doc in response:
            recipe = {
                "recipeId": doc.get("RecipeId"),
                "name": doc.get("Name"),
                "authorId": doc.get("AuthorId"),
                "authorName": doc.get("AuthorName"),
                "cookTime": doc.get("CookTime"),
                "prepTime": doc.get("PrepTime"),
                "totalTime": doc.get("TotalTime"),
                "description": doc.get("Description"),
                "images": doc.get("Images"),
                "category": doc.get("RecipeCategory"),
                "keywords": doc.get("Keywords"),
                "recipeIngredientQuantities": doc.get("RecipeIngredientQuantities"),
                "recipeIngredient": doc.get("RecipeIngredientParts"),
                "rating": doc.get("AggregatedRating"),
                "recipeInstructions": doc.get("RecipeInstructions")
            }

            recipe_details.append(recipe.copy())

        return recipe_details

class UserDetails(object):

    def __init__(self):
        pass

    def get_saved_recipes(self, user_id):
        collection = db.get_collection("users")
        response = collection.find({"_id": user_id})
        # saved_recipe = []

        for user in response:
            saved_recipe = user['saved_array']

        # print(saved_recipe)
        return saved_recipe


@getdata.route('/getrecipebyid', methods=['GET'])
def get_recipe_by_id():

    if (request.args.get('id')):
        recipe_id = int(request.args.get('id'))
        print(id)
        response = collection.find_one({'RecipeId': recipe_id})
        print(response)
        # if response.get("Images") is not None:
        #     images = ast.literal_eval(response.get("Images"))
        # else:
        #     images = "None"
        # if response.get("Keywords") is not None:
        #     keywords = ast.literal_eval(response.get("Keywords"))
        # else:
        #     keywords = "None"
        recipe_details = {
            "recipeId": response.get("RecipeId"),
            "name": response.get("Name"),
            "authorId": response.get("AuthorId"),
            "authorName": response.get("AuthorName"),
            "cookTime": response.get("CookTime"),
            "prepTime": response.get("PrepTime"),
            "totalTime": response.get("TotalTime"),
            "description": response.get("Description"),
            "images": (json.loads(response.get("Images")) if response.get("Images") else response.get("Images")),
            "category": response.get("RecipeCategory"),
            "keywords": (json.loads(response.get("Keywords")) if response.get("Keywords") else response.get("Keywords")),
            "recipeIngredientQuantities": response.get("RecipeIngredientQuantities"),
            "recipeIngredient": ast.literal_eval(response.get("RecipeIngredientParts")),
            "rating": response.get("AggregatedRating"),
            "recipeInstructions": ast.literal_eval(response.get("RecipeInstructions"))
        }

        print(recipe_details)
        return jsonify(recipe_details)

# # recipes = mongo.db.recipes
# # info = mongo.cx
# # print(recipes)
#
#
# @getdata.route('/getrecipes', methods=["GET"])
# def get_recipes():
#     res = src.collection.find()
#     data = []
#     for doc in res:
#         data.append(doc.copy())
#     return data