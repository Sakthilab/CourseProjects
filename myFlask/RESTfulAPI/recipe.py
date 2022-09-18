from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)

api = Api(app)

food_list = [
    {
        "id": 0,
        "name": "butter",
        "type": "Dairy product"
    },
    {
        "id": 100,
        "name": "lobster",
        "type": "sea food"
    },
    {
        "id": 2,
        "name": "chicken65",
        "type": "Meat"
    }
]

class allRecipes(Resource):
    def get(self):
        return jsonify(food_list)

    def post(self):
        data = request.get_json()
        food_list.append(data)
        return food_list

class oneRecipe(Resource):
    def get(self, id):
        for i in food_list:
            if i["id"] == id:
                return jsonify(i)
        else:
            return("Not in list")

    def delete(self, id):
        for i in food_list:
            if i["id"] == id:
                food_list.remove(i)
                return jsonify(food_list)

    def put(self, id):
        for i in food_list:
            if i["id"] == id:
                data1 = request.get_json()
                i.update(data1)
                return jsonify(i)
        else:
            return("Not in list")

api.add_resource(allRecipes, "/recipes")
api.add_resource(oneRecipe, "/recipe/<int:id>")
app.run()