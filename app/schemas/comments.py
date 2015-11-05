from marshmallow import Schema, fields, ValidationError, validates
from app.models import Categories
from sqlalchemy import func
from app.models import Comments
from .base import ResourceSchema, Schema
from app.utils import Method, Role


class CommentSchema(Schema):
    dateCreated = fields.DateTime()
    lastModified = fields.DateTime()

    class Meta:
        fields = Comments.get_columns(Method.READ, Role.ADMIN)


class CommentResourceSchema(ResourceSchema):
    class Meta:
        type = 'comments'


create_comment_serializer = CommentResourceSchema(
    CommentSchema
)

update_comment_serializer = CommentResourceSchema(
    CommentSchema,
    param={'only': set(Comments.get_columns(Method.UPDATE, Role.USER)) - {'parentId', 'userId', 'articleId'}}
)

read_comment_serializer = CommentResourceSchema(
    CommentSchema,
    param={'only': set(Comments.get_columns(Method.READ, Role.GUEST)) - {'parentId', 'userId', 'articleId'}}
)
