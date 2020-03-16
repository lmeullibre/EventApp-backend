from flask import Flask, Blueprint
from flask_cors import CORS
from api.restplus import api
from database import db
import settings

from api.events.endpoints.event import ns as event_namespace
from api.events.endpoints.report import ns as report_namespace
from api.users.endpoints.user import ns as user_namespace
from api.auth.endpoints.auth import ns as auth_namespace
from api.comments.endpoints.comment import ns as comment_namespace

app = Flask(__name__)
CORS(app)


def configure_app(flask_app):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(event_namespace)
    api.add_namespace(user_namespace)
    api.add_namespace(auth_namespace)
    api.add_namespace(comment_namespace)
    api.add_namespace(report_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


def main():
    initialize_app(app)

    app.run(debug=settings.FLASK_DEBUG, host='0.0.0.0')


if __name__ == "__main__":
    main()
