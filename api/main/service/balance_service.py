import os
import random

from api.main.model.user_balance import UserBalances
from api.main import db
from api.main.util import logger

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
    current.subtract(amount)
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

