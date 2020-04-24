from flask_restplus import Api
from flask import Blueprint

from api.main.controller.commitments_controller import api as comm_ns
from api.main.controller.answers_controller import api as ans_ns
from api.main.controller.balance_controller import api as bal__ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )
          
# Routes
api.add_namespace(comm_ns, path='/commitments')
api.add_namespace(ans_ns, path='/answers')
api.add_namespace(bal__ns, path='/balances')