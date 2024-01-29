from flask import Flask
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from app.models import Users
from app.db import db
from app import config
from datetime import timedelta
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.TEST_DB if app.config['TESTING'] else config.SP_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret' # Change this!
app.config["TESTING"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
jwt = JWTManager(app)
ma = Marshmallow(app)
db.init_app(app)

print("##### #### STARTING APPLICATION ### ######")
with app.app_context():
    try:
        db.create_all()
    except:
        pass
    admin_user = Users.query.filter_by(email='admin@example.com').first()
    if not admin_user:
        # create an admin user
        print("Creating admin . . .")
        admin_user = Users(email='admin@example.com', password='password', fullname='Admin', photo='')
        db.session.add(admin_user)
        db.session.commit()
        print("Admin Created")

from app import routes