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
        to_exclude=get_random()
    )
    new_commitment.save()
    return {
        'status': 'success',
        'message': 'Successfully saved commitment.',
        'user_id': new_commitment.user_id,
        'to_exclude_answers': new_commitment.to_exclude
    }

def get_commitments_by_user_id(id):
    return UserCommitments.query.filter_by(user_id=id).first()

def get_random():
    return random.randint(0, get_k()-1)

def validate_length(commitment_list):
    k = get_k()
    if len(commitment_list) != k:
        raise IncorrectLengthException("Number of commitments incorrect, required: %s - found: %s"%(k, len(commitment_list)))

def get_k():
    k = os.getenv("K")
    return int(k)