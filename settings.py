import os


def getenv(name, default=''):
    return os.environ.get(name, default)


# Flask settings
# FLASK_SERVER_NAME = '146.148.124.161:5000'
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings


SQLALCHEMY_DATABASE_URI = getenv('DATABASE_ENVIRONMENT', 'testing')
if SQLALCHEMY_DATABASE_URI == 'testing':
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
else:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://pes_user:pes2019@35.198.146.153/pes_2019'

SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT Settings
PASSWORD_JWT = "ThisIsATest"

# Image storage settings
IMAGE_BUCKET = "pes-image-bucket"
