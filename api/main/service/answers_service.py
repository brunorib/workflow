import os
import random
import json
from time import sleep

import api.main.service.commitments_service as cs
from api.main.service.rpc_service import RpcClient
from api.main.model.user_commitments import UserCommitments
from api.main import db
from api.main.service.exceptions.commitment_exception import *
from api.main.service.exceptions.rpc_exception import *
from api.main.util import logger

def get_client():
    client = None
    rabbit_mq_url = os.getenv('RABBIT_MQ_URL')
    rabbit_mq_rpc_queue = os.getenv('RABBIT_MQ_QUEUE')
    if rabbit_mq_rpc_queue is None:
        rabbit_mq_rpc_queue = 'rpc_queue'
    if rabbit_mq_url:
        client = RpcClient(rabbit_mq_url, rabbit_mq_rpc_queue)
    return client

def verify_answers(data):
    user_coms = cs.get_commitments_by_user_id(data['user_id'])
    if not user_coms:
        raise NoCommitmentException("No previous commitment for this user")

    commitments = user_coms.get_commitments()
    validate_length(data['answers'], commitments)

    to_blind_sign = commitments.pop(user_coms.to_exclude)

    # AMQP CONNECTION TO WORKER
    logger.info("Started getting AMQP Client")
    RPC_CLIENT = get_client()
    if RPC_CLIENT:
        request = {
            "action": "checkFair",
            "payload": {
                "to_blind_sign": to_blind_sign,
                "to_verify": data['answers'],
                "m_commitments": commitments
            },
        }

        logger.info("Sending request")
        corr_id = RPC_CLIENT.send_request(json.dumps(request))

        # Wait until we have received a response.
        while RPC_CLIENT.queue[corr_id] is None:
            logger.info("Waiting request")
            sleep(3)

        logger.info("Got message")
        # Return the response to the user.
        return RPC_CLIENT.queue[corr_id]
    else:
        raise RPCClientException()


def validate_length(answers, coms):
    answers_should = len(coms)-1
    if len(answers) != answers_should:
        raise IncorrectLengthException("Invalid answers length, should be %d and is %s"%(answers_should, len(answers)))