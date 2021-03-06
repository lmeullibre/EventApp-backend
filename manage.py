import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, configure_app
from database import db

configure_app(app)
migrate = Migrate(app, db, compare_type=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
