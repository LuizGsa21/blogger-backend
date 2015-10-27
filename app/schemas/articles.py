from marshmallow import Schema, fields
from app.models import Articles
from .base import ResourceSchema


class ArticleSchema(Schema):
    dateCreated = fields.DateTime()
    lastModified = fields.DateTime()

    class Meta:
        fields = ('title', 'body', 'dateCreated', 'lastModified')


article_serializer = ArticleSchema()


class ArticleResourceSchema(ResourceSchema):
    __model__ = Articles
    __serializer__ = article_serializer

    type = fields.String('articles')


article_resource_serializer = ArticleResourceSchema()
