# api/models.py
import json
from api.main import db
from api.main.model.exceptions.balance_exception import NoSufficientMoneyException

class UserBalances(db.Model):
    """This class represents the balance of money for a user."""
    __tablename__ = 'balances'

    user_id = db.Column(db.Integer, primary_key=True)
    money = db.Column(db.Integer)

    def __init__(self, user_id, money):
        self.user_id = user_id
        self.money = money

    def add_money(self, amount):
        self.money += amount
    
    def subtract_money(self, amount):
        if amount < self.money:
            self.money -= amount
        else:
            raise NoSufficientMoneyException("Not enough money to subtract")

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return UserBalances.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Commmitments of: {}>".format(self.user_id)