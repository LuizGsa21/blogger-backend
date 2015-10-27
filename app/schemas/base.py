from marshmallow import Schema, fields, validates_schema, ValidationError, pre_dump
from app.models import Users
from .schema_helpers import require



class ResourceSchema(Schema):
    __model__ = None
    __serializer__ = None

    id = fields.Function(lambda obj: obj.id)
    attributes = fields.Method('get_attributes')
    links = fields.Function(lambda obj: {'self': obj.url})

    @property
    def type(self):
        raise NotImplemented

    def get_attributes(self, data):
        if isinstance(data, self.__model__):
            return self.__serializer__.dump(data).data
        else:
            return self.__serializer__.dump((data['data']['attributes'])).data