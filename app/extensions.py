from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# from flask_wtf import CsrfProtect
# csrf = CsrfProtect()

from flask_mail import Mail, Message
mail = Mail()

from flask_login import LoginManager
login_manager = LoginManager()

from flask_wtf.csrf import CsrfProtect
csrf = CsrfProtect()

from flask_oauthlib.client import OAuth
oauth = OAuth()
