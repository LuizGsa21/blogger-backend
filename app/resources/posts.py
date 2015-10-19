from flask import Blueprint, jsonify
from app.model import Posts

posts_bp = Blueprint('posts', __name__, url_prefix='/api/v1/posts')


@posts_bp.route('', methods=['GET'])
def get_posts():
    return ''

@posts_bp.route('/<int:id>', methods=['GET'])
def get_post_by_id(id):
    return ''

@posts_bp.route('', methods=['POST'])
def post_posts():
    return ''

@posts_bp.route('', methods=['PUT'])
def put_posts():
    return ''

@posts_bp.route('', methods=['DELETE'])
def delete_posts():
    return ''
