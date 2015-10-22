from flask import Blueprint, jsonify, request
from app.models import Articles, Users
from app.schemas import user_post_serializer
from app.extensions import db

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')


@users_bp.route('', methods=['GET'])
def get_users():
    return ''

@users_bp.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    return ''

@users_bp.route('', methods=['POST'])
def post_users():
    data = request.data
    if not data:
        response = jsonify(errors=[{
            'detail': 'No JSON body found.'
        }])
        response.status_code = 400
        return response

    data, errors = user_post_serializer.loads(data)
    if errors:
        response = jsonify(errors=errors)
        # If there is more than one error, use a 400 status code
        if len(errors) > 1:
            response.status_code = 400
        else:
            response.status_code = errors.itervalues().next()[0]['status']
        return response
    user = Users(**data)
    db.session.add(user)
    db.session.commit()
    data.pop('password', None)
    response = jsonify(data={
        'type': 'users',
        'id': user.id,
        'attributes': data,
        'links': {
            'self': user.url
        }
    })
    response.status_code = 201
    return response

@users_bp.route('', methods=['PUT'])
def put_users():
    return ''

@users_bp.route('', methods=['DELETE'])
def delete_users():
    return ''
