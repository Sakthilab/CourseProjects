from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256
from http import HTTPStatus
import jwt, uuid
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity, create_refresh_token


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:welcome$1234@localhost/userdb'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)
jwt = JWTManager()
jwt.init_app(app)

def token_required(f):
    def decorated(*args, **kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            print("Token not found")
            return jsonify({"message": "Token is missing"})
        else:
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
                currentUser = User.query.filter_by(publicid=data["publicid"]).first()
                if currentUser:
                    return f()
                else:
                    return jsonify({"Message": "Invalid token"})
            except:
                return jsonify({"Message": "Invalid Token"})
    return decorated

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    publicid = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)

    @staticmethod
    def addUser(username, password, email, publicid):
        user = User(username=username, password=password, email=email, publicid=publicid)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def getUser(username):
        user = User.query.filter_by(username=username).first()
        return user

    @staticmethod
    def allUser():
        data = User.query.all()
        return data

@app.route('/signup', methods=["POST"])
def signup():
    newUser = request.get_json()
    userPassword = pbkdf2_sha256.hash(newUser["password"])
    publicid = str(uuid.uuid4())
    user = User.allUser()
    for i in user:
        if i.username == newUser["username"]:
            return jsonify({"message": "User with same username is already exist", "status": HTTPStatus.BAD_REQUEST})
    else:
        User.addUser(username=newUser["username"], password=userPassword, email=newUser["email"], publicid=publicid)
        return jsonify({"message": "user added to database", "status": HTTPStatus.OK})

@app.route('/login', methods=["POST"])
def login():
    userCheck = request.get_json()
    username = userCheck["username"]
    password = userCheck["password"]
    user = User.getUser(username=username)
    if pbkdf2_sha256.verify(password, user.password):
        token = jwt.encode({"publicid": user.publicid, "exp": datetime.utcnow()+timedelta(minutes=1)}, app.config['SECRET_KEY'])
        print(token)
        return jsonify({"message": "Greetings, welcome to postman", "status": HTTPStatus.OK, "token": token})
    else:
        return jsonify({"message": "Username or password is incorrect", "status": HTTPStatus.BAD_REQUEST})


@app.route('/users', methods=["GET"])
@token_required
def users():
    data = User.allUser()
    print(data)
    user = []
    for i in data:
        user.append({'id': i.id, 'name': i.username})

    return jsonify((user),{"status": HTTPStatus.OK})

@app.route('/token', methods=['POST'])
def getToken():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.getUser(username=username)
    if user:
        token = create_access_token(identity=username)
        return jsonify({"token": token})
    else:
        return jsonify({"message": "User is not found in database"})


@app.route('/test', methods=["POST", "GET"])
@jwt_required()
def test():
    user = get_jwt_identity()
    return jsonify({"message": "Successful", "user": user})

if __name__ == '__main__':
    app.run(port=5001)


