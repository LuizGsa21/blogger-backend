from flask import Blueprint, jsonify
from app.models import Articles
from app.schemas import article_resource_serializer

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


@articles_bp.route('', methods=['PUT'])
def put_articles():
    return ''


@articles_bp.route('', methods=['DELETE'])
def delete_articles():
    return ''
