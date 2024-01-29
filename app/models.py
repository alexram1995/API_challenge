from app.db import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))
    fullname = db.Column(db.String(80))
    photo = db.Column(db.String(120))

    def __init__(self, email, password, fullname, photo):
        self.email = email
        self.password = password
        self.fullname = fullname
        self.photo = photo

class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.Text)
    priority = db.Column(db.Integer)
    status = db.Column(db.String(80))
    time_since_published = db.Column(db.Interval)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, title, description, priority, status, user_id, time_since_published=None, created_at=None, updated_at=None):
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.time_since_published = time_since_published
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at

class AccessTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, access_token, user_id):
        self.access_token = access_token
        self.user_id = user_id