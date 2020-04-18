import os
import random

from api.main.model.user_commitments import UserCommitments
from api.main import db
from api.main.service.exceptions.commitment_exception import IncorrectLengthException

def save_commitment(data):
    validate_length(data['commits'])
    com = get_commitments_by_user_id(data['user_id'])
    if com:
        com.delete()

    new_commitment = UserCommitments(
        user_id=data['user_id'],
        commitments=data['commits'],
    )
    new_commitment.save()
    return {
        'status': 'success',
        'message': 'Successfully saved commitment.',
        'user_id': new_commitment.user_id
    }

def get_commitments_by_user_id(id):
    return UserCommitments.query.filter_by(user_id=id).first()

def get_random():
    return {
        'exclude': random.randint(0, K-1),
    }

def validate_length(commitment_list):
    if len(commitment_list) != os.getenv("K"):
        raise IncorrectLengthException()