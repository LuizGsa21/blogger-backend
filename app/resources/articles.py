import pprint
from flask import Blueprint, request
from app.models import Articles
from app.schemas import (
    read_article_serializer,
    create_article_serializer,
    update_article_serializer,
    article_resource_serializer
)
from app.extensions import db
from app.utils import login_required, jsonify
import app.utils as utils
from flask_login import current_user
import json

articles_bp = Blueprint('articles', __name__, url_prefix='/api/v1/articles')


@articles_bp.route('', methods=['GET'])
def get_articles():
    articles = Articles.query.all()
    data, errors = read_article_serializer.dump(articles, many=True)
    return jsonify(data=data)


@articles_bp.route('/<int:id>', methods=['GET'])
def get_article_by_id(id):
    article = Articles.query.get(id)
    data, errors = read_article_serializer.dump(article)
    relationship, included = article.get_relationships(included=True)
    data['relationships'] = relationship
    return jsonify(data=data, included=included)


@articles_bp.route('', methods=['POST'])
@login_required
def post_articles():
    data, _ = create_article_serializer.loads(request.data)
    article = Articles(**data['attributes'])
    relationships = data['relationships']
    if current_user.is_admin:
        article.authorId = relationships['author']['id']
    else:
        article.authorId = current_user.id
    article.categoryId = data['relationships']['category']['id']
    db.session.add(article)
    db.session.commit()

    response = jsonify(data=create_article_serializer.dump(article).data)
    response.status_code = 201
    return response


@articles_bp.route('/<int:id>', methods=['PUT'])
@login_required
def put_article_by_id(id):
    article = Articles.query.filter_by(id=id).first()
    if not article:
        raise utils.PageNotFoundError()
    if not current_user.is_admin and article.authorId != current_user.id:
        raise utils.PermissionDeniedError('edit', 'article')

    data, errors, = update_article_serializer.loads(request.data)
    Articles.query.filter_by(id=id).update(data['attributes'])
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    return response


@articles_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_article_by_id(id):
    article = Articles.query.filter_by(id=id).first()
    if not article:
        raise utils.PageNotFoundError()
    if not current_user.is_admin and article.authorId != current_user.id:
        raise utils.PermissionDeniedError('delete', 'article')
    data, _ = article_resource_serializer.loads(request.data)
    db.session.delete(article)
    db.session.commit()
    response = jsonify()
    response.status_code = 204
    return response

