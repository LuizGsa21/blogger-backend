from flask import Flask, g
from .utils import jsonify
from extensions import db, login_manager, csrf, oauth
from flask_login import AnonymousUserMixin as _AnonymousUserMixin
from config import DevelopmentConfig
from models import Categories, Comments, Articles, Users
from .utils import Role, Error, CsrfTokenError
from resources import articles_bp, users_bp, comments_bp, auth_bp, categories_bp

DEFAULT_BLUEPRINTS = (articles_bp, users_bp, comments_bp, auth_bp, categories_bp)


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

    @app.errorhandler(Error)
    def handle_invalid_usage(error):
        response = jsonify(error.get_errors())
        response.status_code = error.status_code
        return response


def configure_extensions(app):
    """ Configure app extension. """
    # flask SQLAlchemy
    db.init_app(app)
    db.create_all(app=app)

    # CSRF Protection
    csrf.init_app(app)

    @csrf.error_handler
    def csrf_error(reason):
        raise CsrfTokenError()

    # mail.init_app(app)

    # flask OAuthlib
    oauth.init_app(app)

    # Login Manger
    login_manager.init_app(app)

    #  Interface for anonymous users
    class AnonymousUserMixin(_AnonymousUserMixin):
        username = 'Guest User'
        firstName = ''
        lastName = ''
        email = ''
        role = Role.GUEST
        is_admin = False

    login_manager.login_view = 'auth.post_login'
    login_manager.session_protection = "strong"
    login_manager.anonymous_user = AnonymousUserMixin


def configure_blueprints(app, blueprints):
    """ Registers blueprints to the applications """
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
