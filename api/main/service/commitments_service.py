import os
import random

from api.main.model.user_commitments import UserCommitments
from api.main import db
from api.main.service.exceptions.commitment_exception import *
from api.main.util import logger

MAX_ALLOWED_RENEWALS=3

def save_commitment(user_id, commitments):
    validate_length(commitments)
    com = get_commitments_by_user_id(user_id)
    count = 0
    if com:
        saved_coms = com.get_commitments()
        if is_same_commitment(saved_coms, commitments):
            return com
        else:
            count = com.count + 1
            if count > MAX_ALLOWED_RENEWALS:
                raise MaxAllowedRenewalsException("The user can't make more commitments before answering. Contact bank.")
            com.delete()

    new_commitment = UserCommitments(
        user_id=user_id,
        commitments=commitments,
        to_exclude=get_random(),
        count=count
    )
    new_commitment.save()
    return new_commitment
    

def get_commitments_by_user_id(id):
    return UserCommitments.query.filter_by(user_id=id).first()

def delete_commitments_by_user_id(id):
    UserCommitments.query.filter_by(user_id=id).first().delete()

def get_random():
    return random.randint(0, get_k()-1)

def is_same_commitment(com1, com2):
    if com1 == com2:
        return True

    logger.debug('com1: [%s]\ncom2: [%s]' % (','.join(com1), ','.join(com2)))
    return False

def validate_length(commitment_list):
    k = get_k()
    if len(commitment_list) != k:
        raise IncorrectLengthException("Number of commitments incorrect, required: %s - found: %s"%(k, len(commitment_list)))

def get_k():
    k = os.getenv("K")
    return int(k)