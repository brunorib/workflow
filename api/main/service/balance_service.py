import os
import random

from api.main.model.user_balance import UserBalances
from api.main import db
from api.main.util import logger

def ingress(user_id, amount):
    logger.debug("Adding amount to user's balance")
    current = get_balance_by_user_id(user_id)
    if current:
        current.add_money(amount)
    else:
        current = UserBalances(
            user_id=user_id,
            money=amount
        )

    current.save()
    logger.debug("Successfully added")
    return current
    

def get_balance_by_user_id(id):
    return UserBalances.query.filter_by(user_id=id).first()

