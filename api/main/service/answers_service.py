import os
import random
import json
from time import sleep

import api.main.service.commitments_service as cs
import api.main.service.balance_service as bs
from api.main.service.rpc_service import client as RPC_CLIENT
from api.main.model.user_commitments import UserCommitments
from api.main.model.commitments_history import CommitmentsHistory
from api.main.model.user_balance import UserBalances
from api.main import db
from api.main.service.exceptions.commitment_exception import *
from api.main.service.exceptions.rpc_exception import *
from api.main.service.exceptions.answer_exception import *
from api.main.util import logger

CONCAT = "|"

def verify_answers(user_id, answers):
    user_coms = cs.get_commitments_by_user_id(user_id)
    if not user_coms:
        raise NoCommitmentException("No previous commitment for this user")

    commitments = user_coms.get_commitments()
    to_save_history = commitments.copy()
    validate_length(answers, commitments)
    
    to_retrieve = validate_consistency(answers)
    if to_retrieve < 0:
        block_user(user_coms)
        raise AnswersDifferException('Values are not the same on all answers, user will be blocked.')

    to_blind_sign = commitments.pop(user_coms.to_exclude)

    # AMQP CONNECTION TO WORKER
    logger.info("Started getting AMQP Client")
    if RPC_CLIENT:
        request = {
            "action": "checkFair",
            "payload": {
                "to_blind_sign": to_blind_sign,
                "to_verify": answers,
                "m_commitments": commitments
            },
        }

        logger.info("Sending request")
        corr_id = RPC_CLIENT.send_request(json.dumps(request))

        # Wait until we have received a response.
        # TODO: create timeout
        while RPC_CLIENT.queue[corr_id] is None:
            sleep(0.1)

        logger.info("Received response")
        # Return the response to the user.
        response = json.loads(RPC_CLIENT.queue[corr_id])
        if 'blind_signature' in response:
            logger.info("Answers verified successfully")
            user_coms.delete()
            history = CommitmentsHistory(
                user_id=user_id,
                commitments=to_save_history
            )
            history.save()
            bs.subtract(user_id, to_retrieve)
            return response
        else:
            raise AnswersNotVerifiedException(response["message"])
    else:
        raise RPCClientException()


def validate_length(answers, coms):
    answers_should = len(coms)-1
    if len(answers) != answers_should:
        raise IncorrectLengthException("Invalid answers length, should be %d and is %s"%(answers_should, len(answers)))

def validate_consistency(answers):
    to_retrieve = get_value_answer(answers[0])
    for answer in answers[1:]:
        val =  get_value_answer(answer)
        if val != to_retrieve:
            return -1
    return to_retrieve

def get_value_answer(answer):
    return int(answer['amount'].split(CONCAT)[0])

def block_user(user_commitments):
    user_commitments.count = UserCommitments.MAX_ALLOWED_RENEWALS + 1
    user_commitments.save()
