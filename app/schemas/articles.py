from marshmallow import Schema, fields
from app.models import Articles
from .base import ResourceSchema, Schema
from app.utils import Method, Role

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

create_article_serializer = ArticleResourceSchema(
    ArticleSchema
)

update_article_serializer = ArticleResourceSchema(
    ArticleSchema, param={'only': Articles.get_columns(Method.UPDATE, Role.USER)}
)

read_article_serializer = ArticleResourceSchema(
    ArticleSchema, param={'only': Articles.get_columns(Method.READ, Role.GUEST)}
)
