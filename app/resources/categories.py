import pprint
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
def get_category_by_id(id):
    category = Categories.query.get(id)
    data, errors = category_resource_serializer.dump(category)
    data['relationships'] = category.get_relationships()
    return jsonify(data=data)


@categories_bp.route('', methods=['POST'])
@admin_required
def post_categories():
    data, _ = category_resource_serializer.loads(request.data)
    category = Categories(**data['attributes'])
    db.session.add(category)
    db.session.commit()
    response = jsonify(data=category_resource_serializer.dump(category).data)
    response.status_code = 201
    return response


@categories_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def put_category_by_id(id):
    response = json.loads(request.data)
    data, errors, = category_resource_serializer.dump(response['data']['attributes'])
    Categories.query.filter_by(id=id).update(data)
    db.session.commit()
    data, errors = category_resource_serializer.dump(Categories.query.get(id))
    return jsonify(data=data)


@categories_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_category_by_id(id):
    Categories.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify(data=None)
