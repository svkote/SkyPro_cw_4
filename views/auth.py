from flask import request, abort
from flask_restx import Resource, Namespace

from implemented import auth_service
from helpers.decorators import auth_required, admin_required

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):

    def post(self):
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if None in [username, password]:
            return abort(400)

        tokens = auth_service.generate_token(username, password)

        if not tokens:
            return abort(401)

        return tokens, 201

    def put(self):

        data = request.json
        token = data.get('refresh_token')

        if token is None:
            return abort(400)

        tokens = auth_service.refresh_token(token)

        return tokens, 201
