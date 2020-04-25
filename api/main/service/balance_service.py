import os
import random
import json
from time import sleep

from api.main.model.user_balance import UserBalances
from api.main import db
from api.main.util import logger
from api.main.service.rpc_service import get_client
from api.main.service.exceptions.rpc_exception import *

CONCAT = "|"

def consume_token(user_id, token):
    logger.debug("Adding amount to user's balance")

     # AMQP CONNECTION TO WORKER
    logger.info("Started getting AMQP Client")
    RPC_CLIENT = get_client()
    if RPC_CLIENT:
        request = {
            "action": "verify",
            "payload": {
                token
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
        if 'status' in response and response['status'] == 'success':
            amount_to_add = get_amount(token['amount'])
            current = get_balance_by_user_id(user_id)
            current.add_money(amount_to_add)
            current.save()
            logger.debug("Successfully added")
            
            return current

        raise TokenNotVerifiedException(response['message'])
    else:
        raise RPCClientException()

    
def ingress(user_id, amount):
    logger.debug("Adding amount to user's balance")
    current = get_balance_by_user_id(user_id)
    current.add_money(amount)
    current.save()
    logger.debug("Successfully added")
    return current
    
def subtract(user_id, amount):
    logger.debug("Subtracting amount to user's balance")
    current = get_balance_by_user_id(user_id)
    current.subtract_money(amount)
    current.save()
    logger.debug("Successfully subtracted")
    return current

def get_balance_by_user_id(id):
    balance = UserBalances.query.filter_by(user_id=id).first()
    if not balance:
        balance = UserBalances(
            user_id=id,
            money=0
        )
        balance.save()
    return balance

def get_amount(amount):
    return int(amount.split(CONCAT)[0])

