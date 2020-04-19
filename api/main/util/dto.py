from flask_restplus import Namespace, fields

class CommitmentsDto:
    api = Namespace('commitments', description='commitments to save to verify with answers')
    commitments = api.model('commitments', {
        'user_id': fields.Integer(required=True, description='user which performed the commitment'),
        'commits': fields.List(fields.String(required=True, description='commitment'))
    })

class AnswersDto:
    api = Namespace('answers', description='answers to verify commitments')
    answer = api.model('answer', {
        'blinding': fields.String(required=True, description='random blinding factor'),
        'amount': fields.String(required=True, description='amount to retrieve concatenated with random string'),
        'id': fields.String(required=True, description='id of retrieval concatenated with random string'),
    })
    answers = api.model('answers', {
        'user_id': fields.Integer(required=True, description='user who answered'),
        'answers': fields.List(fields.Nested(answer))
    })