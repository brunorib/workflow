import os
from flask import request
from flask_restplus import Resource

from api.main.util.dto import AnswersDto
import api.main.service.answers_service as ans
api = AnswersDto.api
_answers = AnswersDto.answers

@api.route('')
class AnswerList(Resource):
    @api.doc('verify the answer and get blind_signed message')
    @api.expect(_answers, validate=True)
    def post(self):
        data = request.json
        try:
            return ans.verify_answers(user_id=data['user_id'], answers=data['answers'])
        except Exception as e:
            return api.abort(422, custom=str(e))