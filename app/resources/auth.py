from flask import Blueprint, jsonify, request
from app.models import Users
from app.schemas import user_resource_serializer
from app.extensions import login_manager
from flask_login import current_user, login_user, logout_user
import json

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
        response = jsonify(data=user_resource_serializer.dump(user).data)
        response.status_code = 200
        return response

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return jsonify(errors={'detail': 'You are not logged in.'})
