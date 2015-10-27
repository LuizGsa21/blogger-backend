from flask import Blueprint, jsonify, request
from app.models import Articles
from app.schemas import article_resource_serializer, article_serializer
from app.extensions import db
import json

articles_bp = Blueprint('articles', __name__, url_prefix='/api/v1/articles')


@articles_bp.route('', methods=['GET'])
def get_articles():
    articles = Articles.query.all()
    data, errors = article_resource_serializer.dump(articles, many=True)
    return jsonify(data=data)


@articles_bp.route('/<int:id>', methods=['GET'])
def get_article_by_id(id):
    article = Articles.query.get(id)
    data, errors = article_resource_serializer.dump(article)
    return jsonify(data=data)


@articles_bp.route('', methods=['POST'])
def post_articles():
    return ''


@articles_bp.route('/<int:id>', methods=['PUT'])
def put_article_by_id(id):
    response = json.loads(request.data)
    data, errors, = article_serializer.dump(response['data']['attributes'])
    Articles.query.filter_by(id=id).update(data)
    db.session.commit()
    data, errors = article_resource_serializer.dump(Articles.query.get(id))
    return jsonify(data=data)


@articles_bp.route('/<int:id>', methods=['DELETE'])
def delete_article_by_id(id):
    Articles.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify(data=None)
