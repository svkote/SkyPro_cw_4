from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service
from helpers.decorators import auth_required, admin_required

user_ns = Namespace('users')


@user_ns.route('/')
class UserView(Resource):
    # @auth_required
    def get(self):
        users = user_service.get_all()
        res = UserSchema(many=True).dump(users)
        return res, 200

    # @auth_required
    def post(self):
        data = request.json
        new_user = user_service.create(data)
        return '', 201, {'location': f'/users/{new_user.id}'}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    # @auth_required
    def get(self, uid):
        user = user_service.get_user_by_id(uid)
        user_schema = UserSchema().dump(user)
        return user_schema, 200

    # @admin_required
    def post(self, uid):
        data = request.json

        if 'id' not in data:
            data['id'] = uid

        new_user = user_service.update(data)
        return '', 201, {'location': f'/users/{new_user.id}'}

    # @admin_required
    def delete(self, uid):
        user_service.delete(uid)
        return '', 204
