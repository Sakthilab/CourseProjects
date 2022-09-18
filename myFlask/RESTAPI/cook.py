from flask import Flask, request, jsonify

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

app = Flask(__name__)

@app.route("/recipes", methods=["GET"])
def home():
    if request.method == "GET":
        data = jsonify(food_list)
    return data


@app.route("/recipes/<int:r>", methods=["GET"])
def home_select(r):
    if request.method == "GET":
        for i in food_list:
            if i["id"] == r:
                data = jsonify(i)
                return data
        else:
            return ("Not in list")



@app.route("/recipes/<int:d>", methods=["DELETE"])
def home_delete(d):
    if request.method == "DELETE":
        for i in food_list:
            if i["id"] == d:
                food_list.remove(i)
        data = jsonify(food_list)
    return data

@app.route("/recipes/<int:d>", methods=["PUT"])
def home_put(d):
    if request.method == "PUT":
        for i in food_list:
            if i["id"] == d:
                data1 = request.get_json()
                i.update(data1)
        data = jsonify(food_list)
    return data

@app.route('/recipes', methods=["POST"])
def update_data():
    if request.method == "POST":
        data1 = request.get_json()
        food_list.append(data1)

    return food_list

app.run()