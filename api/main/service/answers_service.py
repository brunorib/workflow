import os
import random

import api.main.service.commitments_service as cs
from api.main.service.rpc_service import RpcClient
from api.main.model.user_commitments import UserCommitments
from api.main import db
from api.main.service.exceptions.commitment_exception import *
from api.main.service.exceptions.rpc_exception import *

def get_client():
    client = None
    rabbit_mq_url = os.getenv('RABBIT_MQ_URL')
    if rabbit_mq_url:
        client = RpcClient(rabbit_mq_url)
    return client

def verify_answers(data):
    user_coms = cs.get_commitments_by_user_id(data['user_id'])
    if not user_coms:
        raise NoCommitmentException("No previous commitment for this user")

    commitments = user_coms.get_commitments()
    validate_length(data['answers'], commitments)

    to_blind_sign = commitments.pop(user_coms.to_exclude)

    # AMQP CONNECTION TO WORKER
    client = get_client()
    if client:
        request = {
            "action": "checkFair",
            "payload": {
                "to_blind_sign": to_blind_sign,
                "to_verify": data['answers'],
                "m_commitments": commitments
            },
        }
        result = client.call(request)
        return result
    else:
        raise RPCClientException()


def validate_length(answers, coms):
    answers_should = len(coms)-1
    if len(answers) != answers_should:
        raise IncorrectLengthException("Invalid answers length, should be %d and is %s"%(answers_should, len(answers)))