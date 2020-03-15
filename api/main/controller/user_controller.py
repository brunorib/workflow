from flask import request
from flask_restplus import Resource

from api.main.util.dto import UserDto
from api.main.service.user_service import save_new_user, get_all_users, get_user, get_user_by_username, delete_user, modify_user

api = UserDto.api
_user = UserDto.user

@api.route('')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='users')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)

@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, id):
        """get a user given its identifier"""
        user = get_user(id)
        if not user:
            api.abort(404)
        else:
            return user

    @api.doc('modify a user')
    @api.expect(_user, validate=True)
    @api.marshal_with(_user)
    def put(self, id):
        """modify a user given its identifier"""
        to_modify = request.json
        return modify_user(id, to_modify)

    @api.doc('delete a user')
    @api.marshal_with(_user)
    def delete(self, id):
        """delete a user given its identifier"""
        user = delete_user(id)
        if not user:
            api.abort(404)
        else:
            return user