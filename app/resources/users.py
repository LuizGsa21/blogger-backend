import pprint
import json
from flask import Blueprint, jsonify, request
from app.models import Articles, Users
from app.schemas import user_post_serializer, user_serializer, user_resource_serializer
from app.extensions import db

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')


@users_bp.route('', methods=['GET'])
def get_users():
    users = Users.query.all()
    data, errors = user_resource_serializer.dump(users, many=True)
    return jsonify(data=data)


@users_bp.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    users = Users.query.get(id)
    data, errors = user_resource_serializer.dump(users)
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
    response = jsonify(data=user_resource_serializer.dump(user).data)
    response.status_code = 201
    return response


@users_bp.route('/<int:id>', methods=['PUT'])
def put_users_by_id(id):
    response = json.loads(request.data)
    data, errors, = user_serializer.dump(response['data']['attributes'])
    Users.query.filter_by(id=id).update(data)
    db.session.commit()
    return jsonify(data=user_resource_serializer.dump(Users.query.get(id)).data)


@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_users_by_id(id):
    Users.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify(data=None)
