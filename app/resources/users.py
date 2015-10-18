from flask import Blueprint, jsonify
from app.model import Posts

users_bp = Blueprint('api', __name__, url_prefix='/api/users')


@users_bp.route('/', methods=['GET'])
def get_users():
    pass


@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user_by_id(id):
    pass
