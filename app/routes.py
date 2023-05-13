from app import app, db
from app.models import User, Publication, AccessTokens
from app.schemas import UserSchema, PublicationSchema, AccessTokenSchema
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token,get_jwt_identity, verify_jwt_in_request
import datetime, re

user_schema = UserSchema()
users_schema = UserSchema(many=True)
publication_schema = PublicationSchema()
publications_schema = PublicationSchema(many=True)

@app.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    password = request.json['password']
    fullname = request.json['fullname']
    photo = request.json.get('photo', None)

    # Email validation
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(email_regex, email):
        return jsonify(message='Invalid email'), 400

    # Password validation
    password_regex = r'[A-Za-z0-9@#$%^&+=]{8,}'
    if not re.fullmatch(password_regex, password):
        return jsonify(message='Invalid password: At least 8 characters'), 400
    
     # Validate if it exists already
    if User.query.filter_by(email=email).first():
        return jsonify(message='Invalid email: email already used in another account'), 400
    
    new_user = User(email=email, password=password, fullname=fullname, photo=photo)
    db.session.add(new_user)
    db.session.commit()  
    return user_schema.jsonify(new_user)

@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        # Check if the user already has an access token.
        user_id = user.id
        if AccessTokens.query.filter_by(user_id=user_id).first():
            return jsonify(message='User already logged in'), 200
        else:
            token = create_access_token(identity=user.id)
            access_token = AccessTokens(access_token=token, user_id=user_id)
            db.session.add(access_token)
            db.session.commit()
            return AccessTokenSchema().dump(access_token)
            
    else:
        return jsonify(message='Invalid email or password'), 401

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout_user():
    current_user = get_jwt_identity()
    # Query the database for the user's access token.
    access_token = AccessTokens.query.filter_by(user_id=current_user).first()

    # Delete the access token from the database.
    db.session.delete(access_token)
    db.session.commit()
    return jsonify(message='Successfully logged out'), 200

@app.route('/users/<int:user_id>')
@jwt_required()
def get_user(user_id):
    # Get the user from the database.
    user = User.query.get(user_id)

    # If the user does not exist, return a 404 error.
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Return the user as a JSON object.
    return UserSchema().dump(user)

@app.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    # Get the user from the database.
    user = User.query.get(user_id)
    # If the user does not exist, return a 404 error.
    if not user:
        return jsonify({'error': 'User not found'}), 404
    # Get the request body.
    body = request.get_json()
    # Update the user's data.
    for key, value in body.items():
        setattr(user, key, value)
    # Save the user to the database.
    db.session.commit()
    # Return the user as a JSON object.
    return UserSchema().dump(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):

    # Get the user from the database.
    user = User.query.get(user_id)

    # If the user does not exist, return a 404 error.
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Delete the user from the database.
    db.session.delete(user)
    db.session.commit()

    # Return a success message.
    return jsonify({'message': 'User deleted'})

@app.route('/publications', methods=['POST'])
@jwt_required()
def post_publications():

    # Get the request body.
    body = request.get_json()

    # Validate the request body.
    current_user = get_jwt_identity()
    if not current_user:
        return jsonify({'error': 'Unauthorized'}), 401

    if not body:
        return jsonify({'error': 'Invalid request body'}), 400

    # Create a new publication.
    publication = Publication(
        title=body['title'],
        description=body['description'],
        priority=body['priority'],
        status=body['status'],
        user_id=current_user,
        created_at=datetime.datetime.now().astimezone(datetime.timezone.utc)
    )
    db.session.add(publication)
    db.session.commit()
    return PublicationSchema().dump(publication)


@app.route('/publications')
@jwt_required()
def get_all_publications_for_user():
    """
    Gets all publications for a specific user.
    """
    current_user = get_jwt_identity()
    publications = Publication.query.filter_by(user_id=current_user).all()
    print(publications)
    return PublicationSchema(many=True).dump(publications)

@app.route('/publications/<int:publication_id>', methods=['PUT'])
@jwt_required()
def update_existing_publication(publication_id):
    """
    Updates an existing publication in the database.
    """
    # Get the request body.
    body = request.get_json()
    
    current_user = get_jwt_identity()
    # Validate the request body.
    if not body:
        return jsonify({'error': 'Invalid request body'}), 400

    # Get the publication from the database.
    publication = Publication.query.get(publication_id)
    if not publication:
        return jsonify({'error': 'Invalid id'}), 400
    elif current_user != publication.user_id:
         return jsonify({'error': 'You can only modify your publications'}), 403
    # Update the publication.
    publication.title = body['title']
    publication.description = body['description']
    publication.priority = body['priority']
    publication.status = body['status']
    publication.updated_at=datetime.datetime.now().astimezone(datetime.timezone.utc)
    # Commit the changes to the database.
    db.session.commit()
    # Return the updated publication.
    return PublicationSchema().dump(publication)

@app.route('/publications/<int:publication_id>', methods=['DELETE'])
@jwt_required()
def delete_publication(publication_id):
    """
    Deletes a publication from the database.
    """
    current_user = get_jwt_identity()
    publication = Publication.query.get(publication_id)
    if publication.user_id != current_user:
        return jsonify({'error': 'You can only delete your publications'}), 403

    if not publication:
        return jsonify({'error': 'Invalid id'}), 400
    
    db.session.delete(publication)
    db.session.commit()
    return jsonify({'msg': 'Deleted', "publication_id":publication_id}), 200