from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_mail import Mail


ALLOWED_EXTENSIONS = ['jpg','png', 'jpeg']

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)

app.config['UPLOADS_IMAGE'] = "./navtarang/static/uploads"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///navtarang.db'
app.config['SECRET_KEY']='eeabbb05e00dd85dd374f201dbe371a861a47fe8cd371dffa87fda6b23fced22'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=20)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

login_manager.login_view = "login_page"
login_manager.login_message="Please Login or Create new one! Thanks"
login_manager.login_message_category = 'info'
login_manager.refresh_view = "refresh_page"
login_manager.needs_refresh_message = "For security reasons please Login Again"
login_manager.needs_refresh_message_category= 'danger'


from navtarang import models
from navtarang.routes import Routes
