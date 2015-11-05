from marshmallow import Schema, fields
from app.models import Categories
from .base import ResourceSchema, Schema
from app.utils import Method, Role


class CategorySchema(Schema):
    dateCreated = fields.DateTime()
    lastModified = fields.DateTime()

    class Meta:
        fields = ('id', 'name')


class CategoryResourceSchema(ResourceSchema):
    class Meta:
        type = 'categories'


category_serializer = CategorySchema()
category_resource_serializer = CategoryResourceSchema(CategorySchema)

