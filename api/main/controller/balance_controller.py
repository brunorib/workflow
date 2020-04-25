import os
import json
from flask import request
from flask_restplus import Resource

from api.main.util.dto import BalanceDto
from api.main.service.exceptions.balance_exception import *
import api.main.service.balance_service as bs
api = BalanceDto.api
_ingress = BalanceDto.ingress
_token_payload = BalanceDto.token_payload
        
@api.route('/<id>')
@api.param('id', 'The User Identifier')
@api.response(404, 'User not found.')
class Balance(Resource):
    @api.doc('get a user balance')
    def get(self, id):
        balance = bs.get_balance_by_user_id(id)
        return balance.to_json()
    
    @api.doc('Ingress money on the user balance')
    @api.expect(_ingress, validate=True)
    def put(self, id):
        data = request.json
        balance = bs.ingress(id, data['amount'])
        return balance.to_json()

@api.route('/token')
@api.response(404, 'User not found.')
class TokenConsumer(Resource):
    @api.doc('Ingress money with token on the user balance')
    @api.expect(_token_payload, validate=True)
    def post(self):
        data = request.json
        try:
            balance = bs.consume_token(user_id=data['user_id'], token=data['token'])
            return balance.to_json()
        except TokenNotVerifiedException as e:
            api.abort(422, custom=str(e))