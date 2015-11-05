from flask import Blueprint, request
from app.utils import jsonify, PageNotFoundError, login_required
from app.models import Comments
from app.schemas import read_comment_serializer, create_comment_serializer
comments_bp = Blueprint('comments', __name__, url_prefix='/api/v1/comments')


@comments_bp.route('', methods=['GET'])
def get_comments():
    comments = Comments.query.all()
    data, _ = read_comment_serializer.dump(comments, many=True)
    return jsonify(data=data)

@comments_bp.route('/<int:id>', methods=['GET'])
def get_comment_by_id(id):
    comment = Comments.query.get(id)
    if not comment:
        raise PageNotFoundError()
    data, _ = read_comment_serializer.dump(comment)
    return jsonify(data=data)

@comments_bp.route('', methods=['POST'])
@login_required
def post_comments():
    data, _ = create_comment_serializer.loads(request.data)

    return ''

@comments_bp.route('', methods=['PUT'])
@login_required
def put_comments():
    return ''

@comments_bp.route('', methods=['DELETE'])
@login_required
def delete_comments():
    return ''
