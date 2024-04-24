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
from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound


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

def generate_token(user):
    timestamp = datetime.utcnow()
    payload = {
        "sub": user,
        "iat": timestamp,
        "exp": timestamp + timedelta(minutes=10)
    }

    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    return token

###
# Routing for your application.
###

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

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
 return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"error": "Invalid request, JSON data expected"}), 400
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password,password):
            data = {
                    "message": f"{user.username} successfully logged in.",
                    "token": generate_token(user.username),
                    "id": user.id
                    }
                    
            return jsonify(data), 200

        else:
            data = {
                "message": "Username or password is incorrect"
            }
            
            return jsonify(data), 401
    else:
        login_user();
        data ={
                "message": "Username or password is incorrect"
            }
        return jsonify(data), 401

@app.route("/api/v1/auth/logout", methods=['POST'])
@requires_auth
def logout():
    auth = request.headers.get('Authorization', None)
    blocked_tokens.add(auth)
    return jsonify({'message': 'User logged out successfully'}), 200

@app.route("/api/v1/users/<int:user_id>/posts",methods=["POST"])
@requires_auth
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
            "caption":caption,
            "message": "Post successfully created!"
        }
        return jsonify(data), 201
    else:
        data = {
            "errors":[
                {error.split(" - ")[0]:error.split(" - ")[1]} for error in form_errors(form)
                    ]
        }
        
        return jsonify(data),500
    
@app.route("/api/v1/users/<int:user_id>/posts",methods=["GET"])
@requires_auth
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

@app.route("/api/users/<int:user_id>/follow", methods=["POST"])
@requires_auth
def follow_user(user_id):
    try:
        #implementation of this would depend on how the vueJS side sends over the information on who is to be followed
        # variable should be target user's ID
        current_user_id = request.json.get('current_user_id')['_rawValue']
        
        if current_user_id == user_id:
            return jsonify({'error': 'You cannot follow your own account'}), 400


        # target_user_to_follow = request.form.get('target_user_id')

        target = db.session.query(User).filter_by(id=user_id).first()
        if not target:
            return jsonify({'error': 'Target user not found'}), 404

        follows = Follows(
            user_id= user_id,
            follower_id=current_user_id
        )

        db.session.add(follows)
        db.session.commit()

        data = {
            "message": f"You are now following {target.username}"
        }

        return jsonify(data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/api/v1/posts")
@requires_auth
def get_all_posts():
    posts = []
    try:
        all_posts = db.session.query(Posts).all()

        for post in all_posts:
            try:
                likes_count = db.session.query(func.count(Likes.id)).filter_by(post_id=post.id).scalar()
            except NoResultFound:
                likes_count = 0

            post_dict = {
                "id": post.id,
                "user_id": post.user_id,
                "photo": post.photo,
                "caption": post.caption,
                "created_on": post.created_on,
                "likes": likes_count
            }
            posts.append(post_dict)
        return jsonify(posts=posts),201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/api/v1/posts/<post_id>/like", methods=["POST"])
@requires_auth
def like_post(post_id):
    try:
        #implementation of this would depend on how the vueJS side sends over the information on who is to be followed
        # variable should be target user's ID
        logged_in_user_id =  request.json.get('current_user_id')['_rawValue']
        print(logged_in_user_id)
        like = Likes(
            user_id=logged_in_user_id,
            post_id=post_id
        )

        db.session.add(like)
        db.session.commit()
        try:
            likes_count = db.session.query(func.count(Likes.id)).filter_by(post_id=post_id).scalar()
        except NoResultFound:
            likes_count = 0

        data = {
            "message": "Post liked!",
            "likes": likes_count
        }

        return jsonify(data), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---------------- Additional Endpoints ------------------

# Endppoint to retrieve a specified user
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
@requires_auth
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    profile_data = {
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        'location': user.location,
        'biography': user.biography,
        'profile_photo': user.profile_photo,
        'joined_on': user.joined_on
    }
    return jsonify(profile_data), 200

# Endpoint to retrieve followers for a specific user
@app.route("/api/v1/users/<int:user_id>/follow", methods=["GET"])
@requires_auth
def get_followers(user_id):
    try:
        # Query the database to get the count of followers for the user
        follower_count = db.session.query(Follows).filter_by(user_id=user_id).count()

        data = {
            "user_id": user_id,
            "follower_count": follower_count
        }

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to check if a user is already following another user
@app.route("/api/v1/users/<int:user_id>/is_following", methods=["POST"])
@requires_auth
def is_following(user_id):
    try:
        current_user_id = request.json.get('current_user_id')['_rawValue']

        follows = Follows.query.filter_by(follower_id=current_user_id, user_id=user_id).first()
        is_following = follows is not None

        data = {
            "is_following": is_following
        }

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to check if a user is already liking another users' post
@app.route("/api/v1/posts/<int:post_id>/is_liking", methods=["POST"])
@requires_auth
def is_liking(post_id):
    try:
        current_user_id = request.json.get('current_user_id')['_rawValue']
        
        likes = Likes.query.filter_by(user_id=current_user_id, post_id=post_id).first()
        is_liking = likes is not None

        data = {
            "is_liking": is_liking
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
