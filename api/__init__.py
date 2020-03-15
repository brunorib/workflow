from flask_restplus import Api
from flask import Blueprint

from api.main.controller.user_controller import api as user_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )
          
# Routes
api.add_namespace(user_ns, path='/users')