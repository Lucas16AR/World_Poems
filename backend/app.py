import os
from flask import Flask
from dotenv import load_dotenv
from main import create_app
from main import db

load_dotenv()

app = Flask(__name__)
app = create_app()
app.app_context().push()

@app.route('/')
def index():
    return 'Hello World!!'

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True, port = os.getenv("PORT"))