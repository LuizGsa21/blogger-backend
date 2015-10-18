import os
import json

_absolute_path = os.path.dirname(os.path.abspath(__file__))

# --- WEB CLIENT ID
with open(os.path.join(_absolute_path, os.pardir, 'oauth.json')) as f:
    os.environ.update(json.load(f))

class Config(object):
    PROJECT = 'Programming-Tutorials'
    PROJECT_ROOT = _absolute_path
    STATIC_FOLDER = os.path.join(PROJECT_ROOT, 'static')
    TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT, 'templates')

    # SQLALCHEMY_DATABASE_URI = 'sqlite://'
    # SQLALCHEMY_ECHO = True

    ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif')
    UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, 'uploads')
    MAX_UPLOAD_SIZE = 500 * 1024 ^ 2  # about 500KB

    LOGIN_DISABLED = False
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'how-to-tutorials-development'
    SQLALCHEMY_DATABASE_URI = 'postgresql://vagrant:vagrant@localhost:5432/test'
    # SERVER_NAME = 'ptutorials.mypassion.io'

    GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
    GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']

    FACEBOOK_CLIENT_ID = os.environ['FACEBOOK_CLIENT_ID']
    FACEBOOK_CLIENT_SECRET = os.environ['FACEBOOK_CLIENT_SECRET']

    GITHUB_CLIENT_ID = os.environ['GITHUB_CLIENT_ID']
    GITHUB_CLIENT_SECRET = os.environ['GITHUB_CLIENT_SECRET']

    # EMAIL SETTINGS
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = os.environ['MAIL_USERNAME']
    # MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    # MAIL_DEFAULT_SENDER = os.environ['MAIL_SENDER']