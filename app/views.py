"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""


from flask import jsonify, request, g, send_from_directory, url_for
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from app.forms import *
from .models import *
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
import os
from flask_wtf.csrf import generate_csrf
from datetime import datetime
import jwt
from datetime import datetime, timedelta
from functools import wraps
from time import time
###
# Routing for your application.
###
blocked_tokens = set()

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.headers.get('Authorization', None) # or request.cookies.get('token', None)

    if auth in blocked_tokens:
        return jsonify({'code': 'blocked_token', 'description': 'This token can no longer be used'}), 401

    if not auth:
      return jsonify({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'}), 401

    parts = auth.split()

    if parts[0].lower() != 'bearer':
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'}), 401
    elif len(parts) == 1:
      return jsonify({'code': 'invalid_header', 'description': 'Token not found'}), 401
    elif len(parts) > 2:
      return jsonify({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'}), 401

    token = parts[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

    except jwt.ExpiredSignatureError:
        return jsonify({'code': 'token_expired', 'description': 'token is expired'}), 401
    except jwt.DecodeError:
        return jsonify({'code': 'token_invalid_signature', 'description': 'Token signature is invalid'}), 401

    g.current_user = user = payload
    return f(*args, **kwargs)

  return decorated


@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/register',methods =["POST"])
def register():
    form = Register()
    data = {}
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        location = form.location.data
        bio = form.bio.data
        profile_photo = form.photo.data 
        date_joined = datetime.now()
        photo_name  =  secure_filename(profile_photo.filename)
        profile_photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], photo_name
            ))
        user = User(
        username = username,
        password = hashed_pw,
        firstname = first_name,
        lastname = last_name,
        email = email,
        location = location,
        biography = bio,
        profile_photo = photo_name
        )
        db.session.add(user)
        db.session.commit()
        data =  {
            "message": "User successfully registered",
            "username": username,
            "password": hashed_pw,
            "firstname": first_name,
            "lastname": last_name,
            "email": email,
            "location": location,
            "biography": bio,
            "profile_photo": photo_name,
            "joined_on": date_joined
        }
    
        return jsonify(data),201
    else:
        data = {
            "errors":[
                {error.split(" - ")[0]:error.split(" - ")[1]} for error in form_errors(form)
                    ]
        }
        
        return jsonify(data),500


def generate_token(user):
    timestamp = datetime.utcnow()
    payload = {
        "sub": user,
        "iat": timestamp,
        "exp": timestamp + timedelta(minutes=3)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return token

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    form = Login()
    data = {}
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password,password):
                data = {
                        "message": f"{user.username} successfully logged in.",
                        "token": generate_token(user.username)
                        }
                     
                return jsonify(data), 202

            else:
                data = {
                    "message": "Username or password is incorrect"
                }
                
                return jsonify(data), 401
        else:
            data ={
                    "message": "Username or password is incorrect"
                }
            return jsonify(data), 401

    else:
        data = {
            "errors":[
                {error.split(" - ")[0]:error.split(" - ")[1]} for error in form_errors(form)
                    ]
        }
        return jsonify(data), 500


@app.route("/api/v1/auth/logout", methods=['POST'])
@requires_auth
def logout():
    auth = request.headers.get('Authorization', None)
    blocked_tokens.add(auth)
    return jsonify({'message': 'User logged out successfully'}), 200


@app.route("/api/v1/users/<user_id>/posts",methods=["POST"])
def create_post(user_id):
    form = NewPost()
    if form.validate_on_submit():
        caption = form.caption.data
        photo = form.photo.data 
        photo_name  =  secure_filename(photo.filename)
        photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], photo_name
            ))
        post = Posts(
            caption=caption,
            photo=photo_name,
            user_id=user_id
        )
        db.session.add(post)
        db.session.commit()
        data = {
            "user_id":user_id,
            "photo": photo_name,
            "caption":caption
        }
        return jsonify(data), 201
    else:
        data = {
            "errors":[
                {error.split(" - ")[0]:error.split(" - ")[1]} for error in form_errors(form)
                    ]
        }
        
        return jsonify(data),500
    
@app.route("/api/v1/users/<user_id>/posts",methods=["GET"])
def get_posts(user_id):
    posts = db.session.execute(db.Select(Posts).filter_by(user_id=user_id)).scalars()
    posts =  [
            {
                "id": post.id,
                "user_id": post.user_id,
                "photo": post.photo,
                "caption": post.caption,
                "created_on": str(post.created_on)  
            }
            for post in posts
        ]
    
    return jsonify(posts=posts), 200


@app.route("/api/users/<user_id>/follow", methods=["POST"])
def follow_user(user_id):
    try:
        #implementation of this would depend on how the vueJS side sends over the information on who is to be followed
        # variable should be target user's ID
        target_user_to_follow = request.form.get('target_user_id')

        target = db.session.query(User).filter_by(id=target_user_to_follow).first()
        if not target:
            return jsonify({'error': 'Target user not found'}), 404

        follows = Follows(
            user_id=target_user_to_follow,
            follower_id=user_id
        )

        db.session.add(follows)
        db.session.commit()

        data = {
            "message": f"You are now following {target.username}"
        }

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
