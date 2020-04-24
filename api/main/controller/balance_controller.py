import os
from flask import request
from flask_restplus import Resource

from api.main.util.dto import BalanceDto
import api.main.service.balance_service as bs
api = BalanceDto.api
_ingress = BalanceDto.ingress
        
@api.route('/<id>')
@api.param('id', 'The User Identifier')
@api.response(404, 'User not found.')
class Balance(Resource):
    @api.doc('get a user balance')
    def get(self, id):
        return bs.get_balance_by_user_id(id)
    
    @api.doc('Ingress money on the user balance')
    @api.expect(_ingress, validate=True)
    def put(self, id):
        data = request.json
        return bs.ingress(id, data['amount'])