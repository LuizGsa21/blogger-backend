from flask import Blueprint
from app.utils import jsonify, PageNotFoundError
from app.models import Comments
from app.schemas import comment_resource_serializer
comments_bp = Blueprint('comments', __name__, url_prefix='/api/v1/comments')


@comments_bp.route('', methods=['GET'])
def get_comments():
    comments = Comments.query.all()
    data, _ = comment_resource_serializer.dump(comments, many=True)
    return jsonify(data=data)

@comments_bp.route('/<int:id>', methods=['GET'])
def get_comment_by_id(id):
    comment = Comments.query.get(id)
    if not comment:
        raise PageNotFoundError()
    data, _ = comment_resource_serializer.dump(comment)
    return jsonify(data=data)

@comments_bp.route('', methods=['POST'])
def post_comments():
    return ''

@comments_bp.route('', methods=['PUT'])
def put_comments():
    return ''

@comments_bp.route('', methods=['DELETE'])
def delete_comments():
    return ''
