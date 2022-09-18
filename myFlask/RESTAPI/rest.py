from flask import Flask, request, jsonify

app = Flask(__name__)

user_list=[
    {
        "name": "peter",
        "age": 40
    },
    {
        "name": "Joe",
        "age": 45
    }

]

@app.route('/', methods=["GET"])
def home():
    if request.method == "GET":
        data = jsonify(user_list)
    return data


@app.route('/', methods=["POST"])
def update_data():
    if request.method == "POST":
        data1 = request.get_json()
        user_list.append(data1)

    return user_list

@app.route('/', methods=["DELETE"])
def delete_data():
    if request.method == "DELETE":
        user_list.clear()

    return user_list

@app.route('/<int:age>', methods=["PUT"])
def put_data(age):
    if request.method == "PUT":
        for i in user_list:
            if i["age"] == 45:
                i.update({"name": "joe", "age": age})

    return user_list

app.run()