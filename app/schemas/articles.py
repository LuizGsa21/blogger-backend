from marshmallow import Schema, fields
from app.models import Articles
from .base import ResourceSchema, Schema


class ArticleSchema(Schema):
    dateCreated = fields.DateTime()
    lastModified = fields.DateTime()

    class Meta:
        fields = ('title', 'body', 'dateCreated', 'lastModified')


article_serializer = ArticleSchema()


class ArticleResourceSchema(ResourceSchema):
    class Meta:
        type = 'articles'


article_resource_serializer = ArticleResourceSchema(ArticleSchema)
