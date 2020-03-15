from api.main.model.user import User
from api.main import db

def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            email=data['email'],
            username=data['username']
        )
        save_changes(new_user)
        user_id = get_user_by_username(new_user.username).id
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'id': user_id
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409

def get_all_users():
    return User.query.all()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.filter_by(id=id).first()

def modify_user(id, to_modify):
    user = get_user(id)
    if user:
        user.username = to_modify['username']
        user.email = to_modify['email']
        db.session.commit()
        response_object = {
            'status': 'modified',
            'message': 'User succesfully modified',
            'id': user.id
        }
        return response_object, 204
    else:
        return_not_found(id)


def delete_user(id):
    deleted = User.query.filter_by(id=id).delete()
    if deleted:
        response_object = {
            'status': 'deleted',
            'message': 'User succesfully deleted',
            'id': id
        }
        return response_object, 204
    else:
        return_not_found(id)

def return_not_found(id):
    response_object = {
        'status': 'incomplete',
        'message': 'User not found.',
        'id': id
    }
    return response_object, 404

def save_changes(data):
    db.session.add(data)
    db.session.commit()