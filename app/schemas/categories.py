from marshmallow import Schema, fields, ValidationError, validates
from app.models import Categories
from sqlalchemy import func
from .base import Schema, resource_schema_factory

from app.utils import Method, Role


class CategorySchema(Schema):
    @validates('name')
    def validate_name(self, name):
        category = Categories.query.filter(func.lower(Categories.name) == func.lower(name)).first()
        if category:
            raise ValidationError({'detail': 'Category "%s" already exists.' % name, 'status': 409})

    class Meta:
        fields = Categories.all_columns


create_category_serializer = resource_schema_factory(
    'categories', CategorySchema,
    attributes={'only': Categories.get_columns(Method.CREATE, Role.ADMIN)}
)

read_category_serializer = resource_schema_factory(
    'categories', CategorySchema,
    attributes={'only': Categories.get_columns(Method.READ, Role.GUEST)}
)

update_category_serializer = resource_schema_factory(
    'categories', CategorySchema,
    id={'required': True},
    attributes={'only': Categories.get_columns(Method.UPDATE, Role.ADMIN)}
)

delete_category_serializer = resource_schema_factory(
    'categories', CategorySchema,
    id={'required': True}
)
