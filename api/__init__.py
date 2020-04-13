from flask_restplus import Api
from flask import Blueprint

from api.main.controller.commitments_controller import api as comm_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )
          
# Routes
api.add_namespace(comm_ns, path='/commitments')