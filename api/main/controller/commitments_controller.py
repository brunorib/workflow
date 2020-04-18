import os
from flask import request
from flask_restplus import Resource

from api.main.util.dto import CommitmentsDto
import api.main.service.commitments_service as cs
from api.main.service.exceptions.commitment_exception import *
api = CommitmentsDto.api
_commitments = CommitmentsDto.commitments

@api.route('')
class CommitmentList(Resource):
    @api.response(201, 'Commitments successfully stored.')
    @api.doc('save first commitments of user')
    @api.expect(_commitments, validate=True)
    def post(self):
        data = request.json
        try:
            cs.save_commitment(data=data)
            return cs.get_random()
        except IncorrectLengthException:
            return api.abort(422)

    
@api.route('/k')
class K(Resource)
    @api.doc('get k value')
    def get(self):
        return {
            'k': os.getenv('K')
        }

        
@api.route('/<id>')
@api.param('id', 'The User Identifier')
@api.response(404, 'Commitment not found.')
class Commitment(Resource):
    @api.doc('get a user commitments')
    @api.marshal_with(_commitments)
    def get(self, id):
        """get a commitments given its user identifier"""
        commitments = cs.get_commitments_by_user_id(id)
        if not commitments:
            api.abort(404)
        else:
            return commitments