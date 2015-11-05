import inspect
import pprint
import json
from flask import Blueprint, request
from flask_login import current_user
from app.models import Articles, Users
from app.extensions import db
from app.utils import admin_required, login_required, Error, AdminRequiredError, jsonify
from app.schemas import (
    create_user_serializer,
    create_user_admin_serializer,
    edit_user_profile_serializer,
    edit_user_admin_serializer,
    read_user_serializer
)

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')


@users_bp.route('', methods=['GET'])
def get_users():
    users = Users.query.all()
    data, errors = read_user_serializer.dump(users, many=True)
    return jsonify(data=data)


@users_bp.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    users = Users.query.get(id)
    data, errors = read_user_serializer.dump(users)
    data['relationships'] = users.get_relationships()
    return jsonify(data=data)


@users_bp.route('', methods=['POST'])
def post_users():
    data = request.data
    if not data:
        response = jsonify(errors=[{
            'detail': 'No JSON body found.'
        }])
        response.status_code = 400
        return response
    if current_user.is_admin:
        data, errors = create_user_admin_serializer.loads(data)
    else:
        data, errors = create_user_serializer.loads(data)
    user = Users(**data['attributes'])
    db.session.add(user)
    db.session.commit()
    data, errors = edit_user_profile_serializer.dump(user)
    response = jsonify(data=data)
    response.status_code = 201
    return response


@users_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def put_user_by_id(id):
    # Note: only admins can access this endpoint.
    data, _ = edit_user_admin_serializer.loads(request.data)
    Users.query.filter_by(id=id).update(data['attributes'])
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    return response

@users_bp.route('/<int:id>', methods=['PATCH'])
@login_required
def patch_user_by_id(id):
    if current_user.is_admin:
        data, errors, = edit_user_admin_serializer.loads(request.data)
    elif current_user.id != id:
        raise AdminRequiredError()
    else:
        data, errors, = edit_user_profile_serializer.loads(request.data)
    Users.query.filter_by(id=id).update(data['attributes'])
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    return response


@users_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_user_by_id(id):
    if current_user.id == id:
        response = jsonify(errors=[{'detail': "You can't delete yourself."}])
        response.status_code = 403
        return response
    Users.query.filter_by(id=id).delete()
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    return response
