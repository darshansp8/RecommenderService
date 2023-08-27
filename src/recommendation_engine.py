from flask import Blueprint, request, jsonify
import pickle
# from joblib import load
from src.mongo import RecommendedRecipes, UserDetails


recommend_blueprint = Blueprint("recommend",__name__)
knn_model = pickle.load(open("src/knn_model.pkl", "rb"))
rating_by_user = pickle.load(open("src/rating_by_user.pkl", "rb"))


@recommend_blueprint.route('/', methods=['GET'])
def index():
    return "<h1>Index</h1>"


@recommend_blueprint.route('/recommend', methods=['GET'])
def recommend():
    recipe_ids = {}
    similar_recipes = []
    recommend_recipe = False
    user_details = UserDetails()
    saved_recipe = user_details.get_saved_recipes(1)
    print(saved_recipe)

    # print(recipe_index)
    # if recommend_recipe:
    if len(saved_recipe) > 0:
        print("Inside If length more than 0")
        recommended_recipe = RecommendedRecipes()
        recipe_id_list = list(rating_by_user.index)
        print(recipe_id_list[0])
        for recipe_id in saved_recipe:
            print(recipe_id)
            if recipe_id in recipe_id_list:
                print(f"Recipe Id {recipe_id}, present in the matrix")
                recipe_index = recipe_id_list.index(recipe_id)
                distances, indices = knn_model.kneighbors(rating_by_user.iloc[recipe_index, :].values.reshape(1,-1), n_neighbors=50)
                for i in range(0, len(distances.flatten())):
                    if i == 0:
                        print(f"Recommendation for {recipe_id}")
                    else:
                        # recipe_ids.append(rating_by_user.index[indices.flatten()[i]])
                        similarity = (1 / (1 + distances.flatten()[i]))
                        print(f"{i}: {rating_by_user.index[indices.flatten()[i]]}, with a similarity of {similarity}")
                        recipe_id = int(rating_by_user.index[indices.flatten()[i]])
                        similar_recipe = {
                            'recipe_id': int(rating_by_user.index[indices.flatten()[i]]),
                            'similarity': similarity * 100,
                            # 'recipe_details': {}
                        }
                        # similar_recipe['recipe_details']['similarity'] = similarity
                        # similar_recipe['recipe_details']['recipe_id'] = int(rating_by_user.index[indices.flatten()[i]])
                        if similar_recipe['similarity'] >= 75:
                            # similar_recipe_id = [recipe_id]
                            # _retrieved_recipe = recommended_recipe.get_recipes_by_id(similar_recipe_id)[0]
                            # similar_recipe.update(_retrieved_recipe)
                            similar_recipes.append(similar_recipe.copy())
            else:
                '''
                Recommend recipes based on content
                '''
                pass

        for recipe in similar_recipes:
            similar_recipe_id = [recipe['recipe_id']]
            _retrieved_recipe = recommended_recipe.get_recipes_by_id(similar_recipe_id)[0]
            recipe.update(_retrieved_recipe)
        # similar_recipes_id = [recipe['recipe_id'] for recipe in similar_recipes]
        # print(similar_recipes_id)
        #
        # similar_recipes_details = recommended_recipe.get_recipes_by_id(similar_recipes_id)[0]
        # print(similar_recipes_details)

        return jsonify(similar_recipes)
    else:
        return jsonify({"message": "Rate atleast 1 recipe"})


"""
Previously working code start
"""
    # if request.args.get('recipeId'):
    #     input_recipe = int(request.args.get('recipeId'))
    # else:
    #     input_recipe = None
    #
    #
    # recipe_id_list = list(rating_by_user.index)
    #
    # if input_recipe and input_recipe in recipe_id_list:
    #     recipe_index = recipe_id_list.index(input_recipe)
    #     recommend_recipe = True
"""
Previously working code end
"""