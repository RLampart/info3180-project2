# Add any model classes for Flask-SQLAlchemy here
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key = True)
    caption = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    user_id = db.Column(db.Integer,nullable = False)
    created_on = db.Column(db.DateTime())
    
    
    
    def __init__(self,caption,photo,user_id):
        self.caption = caption
        self.photo = photo
        self.user_id = user_id
        self.created_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def __repr__(self):
        return '<Posts %r>' % self.id
    
class Likes(db.Model) :
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key = True)
    post_id = db.Column(db.Integer,nullable = False)
    user_id  = user_id = db.Column(db.Integer,nullable = False)
    
    def __init__(self,post_id,user_id):
        self.post_id = post_id
        self.user_id = user_id
        
    def __repr__(self):
        return '<Likes %r>' % self.id
    
class Follows(db.Model):
    __tablename__ = 'follows'
    
    id = db.Column(db.Integer(), primary_key = True)
    follower_id = db.Column(db.Integer(), nullable = False)
    user_id = db.Column(db.Integer(), nullable = False)
    
    def __init__(self,follower_id,user_id):
        self.follower_id = follower_id
        self.user_id = user_id
        
    def __repr__(self):
        return '<Follows %r>' % self.id
    
class User(db.Model):
    __tablename__ = 'users' 
    
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(255), nullable = False)
    firstname = db.Column(db.String(255), nullable = False)
    lastname = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255))
    location = db.Column(db.String(255))
    biography = db.Column(db.String(255))
    profile_photo = db.Column(db.String(255))
    joined_on = db.Column(db.DateTime(), nullable = False)
    
    def __init__(self, username, password, firstname, lastname, email, location, biography, profile_photo):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname =  lastname
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = profile_photo
        self.joined_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
    
