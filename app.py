from flask import Flask
from flask_restx import Api

from config import Config
from dao.model.user import User
from implemented import user_service
from setup_db import db
from views.auth import auth_ns
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def create_data(app, db):
    with app.app_context():
        db.create_all()

        users = [
            {'username': "vasya", 'password': "my_little_pony", 'role': "user"},
            {'username': "oleg", 'password': "qwerty", 'role': "user"},
            {'username': "oleg", 'password': "P@ssw0rd", 'role': "admin"}
        ]

        for user in users:
            user_service.create(user)


def register_extensions(app):
    db.init_app(app)
    create_data(app, db)

    with app.app_context():
        db.create_all()
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(debug=True)
