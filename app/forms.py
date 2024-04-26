from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, PasswordField, EmailField
from wtforms.validators import InputRequired, Email
from flask_wtf.file import FileField,FileRequired,FileAllowed


class Register(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired(), Email()])
    location = StringField('Location', validators=[InputRequired()])
    bio = TextAreaField('Biography', validators=[InputRequired()])
    photo = FileField('Upload Photo', validators=[
        FileRequired(message='Please upload profile photo'),
        FileAllowed(['jpg', 'png'], message='Only JPEG and PNG images are allowed.')
    ])



class NewPost(FlaskForm):
    photo = FileField('Upload Poster', validators=[
        FileRequired(message='Please upload a photo'),
        FileAllowed(['jpg', 'png'], message='Only JPEG and PNG images are allowed.')
    ])
    caption = TextAreaField('Caption', validators=[InputRequired()])