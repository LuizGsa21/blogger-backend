from flask import Blueprint, request
from app.utils import jsonify, PageNotFoundError, PermissionDeniedError, login_required
from app.models import Comments
from app.extensions import db
from app.schemas import (
    read_comment_serializer,
    create_comment_serializer,
    update_comment_serializer
)
from flask_login import current_user

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
    relationships = data['relationships']
    userId = relationships['user']['id']

    if not current_user.is_admin and userId != str(current_user.id):
        raise PermissionDeniedError('create', 'comment')
    attributes = data['attributes']
    attributes['userId'] = userId
    attributes['articleId'] = relationships['article']['id']
    attributes['parentId'] = relationships['comment']['id']
    comment = Comments(**attributes)
    db.session.add(comment)
    db.session.commit()
    response = jsonify(data=create_comment_serializer.dump(comment).data)
    response.status_code = 201
    return response

@comments_bp.route('/<int:id>', methods=['PUT'])
@login_required
def put_comment_by_id(id):
    comment = Comments.query.filter_by(id=id).first()
    if not comment:
        raise PageNotFoundError()
    if not current_user.is_admin and comment.userId != current_user.id:
        raise PermissionDeniedError('edit', 'comment')
    data, _ = update_comment_serializer.loads(request.data)
    Comments.query.filter_by(id=id).update(data['attributes'])
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    return response

@comments_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_comment_by_id(id):
    comment = Comments.query.filter_by(id=id).first()
    if not comment:
        raise PageNotFoundError()
    if not current_user.is_admin and comment.userId != current_user.id:
        raise PermissionDeniedError('delete', 'comment')
    data, _ = read_comment_serializer.loads(request.data)
    db.session.delete(comment)
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    return response
