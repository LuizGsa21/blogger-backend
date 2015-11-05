from marshmallow import Schema, fields, ValidationError, validates
from app.models import Categories
from sqlalchemy import func
from .base import ResourceSchema, Schema

from app.utils import Method, Role


class CategorySchema(Schema):
    @validates('name')
    def validate_name(self, name):
        category = Categories.query.filter(func.lower(Categories.name) == func.lower(name)).first()
        if category:
            raise ValidationError({'detail': 'Category "%s" already exists.' % name, 'status': 409})

    class Meta:
        fields = ('id', 'name')


class CategoryResourceSchema(ResourceSchema):
    class Meta:
        type = 'categories'


category_serializer = CategorySchema()
category_resource_serializer = CategoryResourceSchema(CategorySchema)
