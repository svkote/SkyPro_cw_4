from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from implemented import director_service
from helpers.decorators import auth_required, admin_required
from parsers import page_parser

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        filters = page_parser.parse_args()
        rs = director_service.get_all(filters)
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.json
        new_director = director_service.create(data)
        return '', 201, {'location': f'/directors/{new_director.id}'}


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    @auth_required
    def get(self, rid):
        r = director_service.get_one(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200

    @admin_required
    def post(self, rid):
        data = request.json

        if 'id' not in data:
            data['id'] = rid

        new_director = director_service.update(data)
        return '', 201, {'location': f'/directors/{new_director.id}'}

    @admin_required
    def delete(self, rid):
        director_service.delete(rid)
        return '', 204
