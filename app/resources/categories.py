from flask import Blueprint, jsonify, request
from app.models import Categories
from app.schemas import category_resource_serializer
from app.extensions import db
from app.utils import admin_required
import json

categories_bp = Blueprint('categories', __name__, url_prefix='/api/v1/categories')


@categories_bp.route('', methods=['GET'])
def get_categories():
    categories = Categories.query.all()
    data, errors = category_resource_serializer.dump(categories, many=True)
    return jsonify(data=data)


@categories_bp.route('/<int:id>', methods=['GET'])
def get_article_by_id(id):
    article = Categories.query.get(id)
    data, errors = category_resource_serializer.dump(article)
    data['relationships'] = article.get_relationships()
    return jsonify(data=data)


@categories_bp.route('', methods=['POST'])
@admin_required
def post_categories():
    return ''


@categories_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def put_article_by_id(id):
    response = json.loads(request.data)
    data, errors, = category_resource_serializer.dump(response['data']['attributes'])
    Categories.query.filter_by(id=id).update(data)
    db.session.commit()
    data, errors = category_resource_serializer.dump(Categories.query.get(id))
    return jsonify(data=data)


@categories_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_article_by_id(id):
    Categories.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify(data=None)
