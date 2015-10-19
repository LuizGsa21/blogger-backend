from flask import Blueprint, jsonify
from app.model import Posts

users_bp = Blueprint('users', __name__, url_prefix='/api/v1/users')


@users_bp.route('', methods=['GET'])
def get_users():
    return ''

@users_bp.route('/<int:id>', methods=['GET'])
def get_user_by_id(id):
    return ''

@users_bp.route('', methods=['POST'])
def post_users():
    return ''

@users_bp.route('', methods=['PUT'])
def put_users():
    return ''

@users_bp.route('', methods=['DELETE'])
def delete_users():
    return ''
