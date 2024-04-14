"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from flask import Flask, make_response, request, jsonify
from app import app
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from app.forms import *
from .models import *
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from app import app, db
import os
from flask_wtf.csrf import generate_csrf
from datetime import datetime

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
        password = generate_password_hash(password),
        firstname = first_name,
        lastname = last_name,
        email = email,
        location = location,
        biography = bio,
        profile_photo = photo_name
        )
        db.session.add(user)
        db.session.commit()
        data = {
            "message": "User successfully registered",
            "username": username,
            "password": password,
            "firstname": first_name,
            "lastname": last_name,
            "email": email,
            "location": location,
            "biography": bio,
            "profile_photo": photo_name,
            "joined_on": date_joined
        }
    else:
        data = {
            "errors":[
                {error.split(" - ")[0]:error.split(" - ")[1]} for error in form_errors(form)
                    ]
        }
    return make_response(data,200)
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