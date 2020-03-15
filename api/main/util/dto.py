from flask_restplus import Namespace, fields

from api.main.model.user import User

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'id': fields.Integer(description='user Identifier')
    })