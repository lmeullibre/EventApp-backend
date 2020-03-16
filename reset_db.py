from app import initialize_app, app
from database import reset_database

initialize_app(app)
with app.app_context():
    reset_database()
