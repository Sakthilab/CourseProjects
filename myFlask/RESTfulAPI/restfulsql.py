from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:welcome$1234@localhost/moviesdb'
db = SQLAlchemy(app)


# class Profile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    title = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(80), nullable=False)

    @staticmethod
    def add_movie(title, year, genre):
        new_movie = Movie(title=title, year=year, genre=genre)
        db.session.add(new_movie)
        db.session.commit()

    @staticmethod
    def get_movies():
        data = Movie.query.all()
        return data

    @staticmethod
    def get_movies_id(id):
        data = Movie.query.filter_by(id=id).first()
        return data

    @staticmethod
    def count_data():
        c = Movie.query.count()
        return c


    @staticmethod
    def delete_movie(id):
        new_movie = Movie.query.filter_by(id=id).delete()
        db.session.commit()
        return new_movie

    @staticmethod
    def update_movie(id, title, year, genre):
        movie = Movie.query.filter_by(id=id).first()
        print(movie)
        movie.title=title
        movie.year=year
        movie.genre = genre
        db.session.commit()
        return movie


class AllMovies(Resource):
    def post(self):
        data = request.get_json()
        Movie.add_movie(title=data["title"], year=data["year"], genre=data["genre"])
        return jsonify({"message": "movie added to database", "status": HTTPStatus.OK})

    def get(self):
        data = Movie.get_movies()
        li = []
        for i in data:
            dic = {}
            dic["id"] = i.id
            dic["title"] = i.title
            dic["year"] = i.year
            dic["genre"] = i.genre
            li.append(dic)
        print(li)
        return jsonify((li),{"status": HTTPStatus.OK})

class MovieByID(Resource):
    def get(self, id):
            dic = {}
            data = Movie.get_movies_id(id)
            if data:
                dic["id"] = data.id
                dic["title"] = data.title
                dic["year"] = data.year
                dic["genre"] = data.genre
                return jsonify(dic,{"status": HTTPStatus.OK})
            else:
                return jsonify({"message": "movie not found in  database", "status": HTTPStatus.NOT_FOUND})

    def delete(self, id):
        result = Movie.delete_movie(id)
        if result:
            return jsonify({"message": "movie deleted from database", "status": HTTPStatus.OK})
        else:
            return jsonify({"message": "movie not in database", "status": HTTPStatus.NOT_FOUND})

    def put(self, id):
        data = request.get_json()
        print(data)
        result = Movie.update_movie(id=id, title =data["title"], year= data["year"], genre= data["genre"])
        if result:
            return jsonify({"message": "movie updated successfully", "status": HTTPStatus.OK})
        else:
            return jsonify({"message": "record not found", "status": HTTPStatus.NOT_FOUND})


api.add_resource(AllMovies, "/movies")
api.add_resource(MovieByID, "/movies/<int:id>")
app.run()