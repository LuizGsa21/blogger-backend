from flask import Blueprint, request, session, url_for
from app.models import Users
from app.schemas import view_user_serializer
from app.extensions import login_manager, oauth
from app.utils import jsonify
from flask_login import current_user, login_user, logout_user
from flask_oauthlib.client import OAuthException
import json
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/logout', methods=['POST'])
def post_logout():
    if not current_user.is_authenticated:
        response = jsonify(errors={'detail': 'You are not logged in.'.format(current_user.username)})
        response.status_code = 400
        return response
    logout_user()
    return jsonify(data=None)


@auth_bp.route('/login', methods=['POST'])
def post_login():
    if current_user.is_authenticated:
        response = jsonify(errors={'detail': 'You are already login as {}.'.format(current_user.username)})
        response.status_code = 400
        return response
    data = json.loads(request.data)['data']
    emailOrUsername = data['username']
    if '@' in emailOrUsername:
        user = Users.query.filter(Users.email_insensitive == emailOrUsername).first()
    else:
        user = Users.query.filter(Users.username_insensitive == emailOrUsername).first()

    if not user or not user.check_password(data['password']):
        response = jsonify(errors={
            'detail': 'Invalid username or password.'
        })
        response.status_code = 400
        return response
    else:
        login_user(user, remember=True)
        response = jsonify(data=view_user_serializer.dump(user).data)
        response.status_code = 200
        return response


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return jsonify(errors={'detail': 'You are not logged in.'})

# OAuth GitHub
github = oauth.remote_app(
    'github',
    consumer_key=os.environ['GITHUB_CLIENT_ID'],
    consumer_secret=os.environ['GITHUB_CLIENT_SECRET'],
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)


@auth_bp.route('/oauth/github/authorized')
def github_authorized():
    resp = github.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    session['github_token'] = (resp['access_token'], '')
    me = github.get('user')
    return jsonify(me.data)


@auth_bp.route('/oauth/github/login')
def github_login():
    return github.authorize(callback=url_for('.github_authorized', _external=True))


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')

# OAuth Facebook
facebook = oauth.remote_app(
    'facebook',
    consumer_key=os.environ['FACEBOOK_CLIENT_ID'],
    consumer_secret=os.environ['FACEBOOK_CLIENT_SECRET'],
    request_token_params={'scope': 'email'},
    base_url='https://graph.facebook.com',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    access_token_method='GET',
    authorize_url='https://www.facebook.com/dialog/oauth'
)


@auth_bp.route('/oauth/facebook/login')
def facebook_login():
    return facebook.authorize(callback=url_for('.facebook_authorized', _external=True))


@auth_bp.route('/oauth/facebook/authorized')
def facebook_authorized():
    resp = facebook.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %s' % resp.message

    session['facebook_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    return 'Logged in as id=%s name=%s redirect=%s' % \
           (me.data['id'], me.data['name'], request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('facebook_token')

# OAuth Google

google = oauth.remote_app(
    'google',
    consumer_key=os.environ['GOOGLE_CLIENT_ID'],
    consumer_secret=os.environ['GOOGLE_CLIENT_SECRET'],
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


@auth_bp.route('/oauth/google/login')
def google_login():
    return google.authorize(callback=url_for('.google_authorized', _external=True))


@auth_bp.route('/oauth/google/authorized')
def google_authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return jsonify({"data": me.data})


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
