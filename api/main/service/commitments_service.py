from api.main.model.user_commitments import UserCommitments
from api.main import db

def save_commitment(data):
    com = get_commitments_by_user_id(data['user_id'])
    
    if com:
        com.delete()

    new_commitment = UserCommitments(
        user_id=data['user_id'],
        commitments=data['commitments'],
    )
    new_commitment.save()
    return {
        'status': 'success',
        'message': 'Successfully saved commitment.',
        'user_id': new_commitment.user_id
    }

def get_commitments_by_user_id(id):
    return UserCommitments.query.filter_by(user_id=id).first()