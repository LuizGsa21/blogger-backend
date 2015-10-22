from flask import Blueprint, jsonify
from app.models import Articles

articles_bp = Blueprint('articles', __name__, url_prefix='/api/v1/articles')


@articles_bp.route('', methods=['GET'])
def get_articles():
    return ''

@articles_bp.route('/<int:id>', methods=['GET'])
def get_post_by_id(id):
    return ''

@articles_bp.route('', methods=['POST'])
def post_articles():
    return ''

@articles_bp.route('', methods=['PUT'])
def put_articles():
    return ''

@articles_bp.route('', methods=['DELETE'])
def delete_articles():
    return ''
