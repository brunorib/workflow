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
            com = cs.save_commitment(user_id=data['user_id'], commitments=data['commits'])
            return {
                'status': 'success',
                'message': 'Successfully saved commitment.',
                'user_id': com.user_id,
                'to_exclude_answers': com.to_exclude
            }
        except (IncorrectLengthException, MaxAllowedRenewalsException, AlreadyUsedCommitmentException) as e:
            return api.abort(422, custom=str(e))

    
@api.route('/k')
class K(Resource):
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