from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect 

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
#app.config['WTF_CSRF_ENABLED'] = False #bypass CSRF validation 

migrate = Migrate(app, db) 
from app import models

from app import views
