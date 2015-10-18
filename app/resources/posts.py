from flask import Blueprint, jsonify
from app.model import Posts

posts_bp = Blueprint('api', __name__, url_prefix='/api/posts')


@posts_bp.route('/', methods=['GET'])
def get_posts():
    pass


@posts_bp.route('/posts/<int:id>', methods=['GET'])
def get_post_by_id(id):
    pass


@posts_bp.route('/posts/author/<int:id>', methods=['GET'])
def get_posts_by_author_id(id):
    pass
