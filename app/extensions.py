from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# from flask_wtf import CsrfProtect
# csrf = CsrfProtect()

from flask_oauth import OAuth
oauth = OAuth()

from flask_mail import Mail, Message
mail = Mail()

from flask_login import LoginManager
login_manager = LoginManager()
