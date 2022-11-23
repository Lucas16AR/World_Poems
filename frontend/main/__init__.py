import os
from flask import Flask
from dotenv import load_dotenv


def create_app():
    app=Flask(__name__)
    load_dotenv()
    app.config['API_URL'] = os.getenv('API_URL')
    
    from main.routes import main, poems, users, qualifications
    app.register_blueprint(main.app)
    app.register_blueprint(poems.poems)
    app.register_blueprint(users.users)
    app.register_blueprint(qualifications.qualifications)
    return app