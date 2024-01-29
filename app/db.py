from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.TEST_DB if app.config['TESTING'] else config.SP_DB
db = SQLAlchemy(app)
