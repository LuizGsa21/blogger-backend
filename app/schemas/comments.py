from marshmallow import Schema, fields, ValidationError, validates
from app.models import Categories
from sqlalchemy import func
from .base import ResourceSchema, Schema
from app.utils import Method, Role


class CommentSchema(Schema):
    dateCreated = fields.DateTime()
    lastModified = fields.DateTime()

    class Meta:
        fields = ('title', 'body', 'dateCreated', 'lastModified')


class CommentResourceSchema(ResourceSchema):
    class Meta:
        type = 'categories'


comment_serializer = CommentSchema()
comment_resource_serializer = CommentResourceSchema(CommentSchema)
