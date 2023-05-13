from flask import Flask
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from app.models import User
from app.db import db
from app import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.TEST_DB if app.config['TESTING'] else config.SP_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret' # Change this!
app.config["TESTING"] = False
jwt = JWTManager(app)
ma = Marshmallow(app)
db.init_app(app)

with app.app_context():
    try:
        db.create_all()
    except:
        pass
    admin_user = User.query.filter_by(email='admin@example.com').first()
    if not admin_user:
        # create an admin user
        admin_user = User(email='admin@example.com', password='password', fullname='Admin', photo='')
        db.session.add(admin_user)
        db.session.commit()

from app import routes