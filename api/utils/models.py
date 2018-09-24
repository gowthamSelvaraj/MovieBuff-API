"""Database file."""

import os
from flask_mongoalchemy import BaseQuery, MongoAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

db = MongoAlchemy()


class MyQueries(BaseQuery):

    def get_username(self, user_name):
        return self.filter(self.type.username == user_name)

    def get_movie(self, movie_id):
        return self.filter(self.type.movie_id == movie_id)


class User(db.Document):
    query_class = MyQueries

    first_name = db.StringField()
    last_name = db.StringField()
    username = db.StringField()
    password = db.StringField()

    def generate_token(self, expiration=6000):
        serial = Serializer(os.getenv('SECRET'), expires_in=expiration)
        return serial.dumps({'id': self.password}).decode('utf-8')   

    def verify_auth_token(self, token):
        serial = Serializer(os.getenv('SECRET'))
        try:
            data = serial.loads(token)

        except SignatureExpired:
            return "Expired Token!" # valid token, but expired
        except BadSignature:
            return "Invalid Token!" # invalid token
        user = User.query.get(data['id'])
        return user


class FavouriteMovies(db.Document):
    query_class = MyQueries
    movie_id = db.IntField()
    movie_title = db.StringField()
    popularity = db.FloatField()
    release_date = db.DateTimeField()
    overview = db.StringField()
