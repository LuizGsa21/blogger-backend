from flask import Blueprint, jsonify
from app.models import Comments

comments_bp = Blueprint('comments', __name__, url_prefix='/api/v1/comments')


@comments_bp.route('', methods=['GET'])
def get_comments():
    return ''

@comments_bp.route('/<int:id>', methods=['GET'])
def get_comment_by_id(id):
    return ''

@comments_bp.route('', methods=['POST'])
def post_comments():
    return ''

@comments_bp.route('', methods=['PUT'])
def put_comments():
    return ''

@comments_bp.route('', methods=['DELETE'])
def delete_comments():
    return ''
