# manage.py
import os
import unittest

from werkzeug.utils import cached_property
from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from api.main import db, create_app
from api import blueprint
import ptvsd

address = ('0.0.0.0', 3000)
ptvsd.enable_attach('my_secret', address)

config_name = os.getenv('APP_SETTINGS')
if os.getenv('APP_SETTINGS') is None:
    config_name = 'development'
    
app = create_app(config_name=os.getenv('APP_SETTINGS'))
app.register_blueprint(blueprint)
app.app_context().push()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='0.0.0.0')

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('api/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
    db.create_all()