
from flask import Flask, g
from extensions import db, login_manager
from flask_login import AnonymousUserMixin as _AnonymousUserMixin
from config import DevelopmentConfig
from models import Categories, Comments, Articles, Users
from resources import articles_bp, users_bp, comments_bp, auth_bp

DEFAULT_BLUEPRINTS = (articles_bp, users_bp, comments_bp, auth_bp)


def create_app(app_name=None, blueprints=None, config=None):
    """Creates and returns a Flask application"""

    # Load default settings
    if app_name is None:
        app_name = DevelopmentConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS
    if config is None:
        config = DevelopmentConfig

    app = Flask(app_name, template_folder=config.TEMPLATE_FOLDER, static_folder=config.STATIC_FOLDER)

    app.config.from_object(config)
    configure_extensions(app)
    configure_hook(app)
    configure_blueprints(app, blueprints)

    return app


def configure_hook(app):
    """ Configure app hooks. """
    # @app.before_request
    # def before_request():
    #     g.user = current_user


def configure_extensions(app):
    """ Configure app extension. """
    # flask SQLAlchemy
    db.init_app(app)
    db.create_all(app=app)

    # CSRF Protection
    # csrf.init_app(app)

    # mail.init_app(app)

    # Login Manger
    login_manager.init_app(app)

    #  Interface for anonymous users
    class AnonymousUserMixin(_AnonymousUserMixin):
        username = 'Guest User'
        firstName = ''
        lastName = ''
        email = ''
        is_admin = False

    login_manager.login_view = 'auth.post_login'
    login_manager.session_protection = "strong"
    login_manager.anonymous_user = AnonymousUserMixin

def configure_blueprints(app, blueprints):
    """ Registers blueprints to the applications """
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

