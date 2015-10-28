from marshmallow import Schema, fields, validates_schema, ValidationError, pre_dump, pre_load
from app.models import Users
from .schema_helpers import require
from .base import ResourceSchema

class UserSchema(Schema):

    dateJoined = fields.DateTime()

    class Meta:
        fields = ('username', 'firstName', 'lastName', 'dateJoined', 'avatarPath')

user_serializer = UserSchema()

class UserResourceSchema(ResourceSchema):
    __model__ = Users
    __serializer__ = user_serializer
    type = fields.String('users')

class UserPostSchema(Schema):
    username = fields.String(required=require('username'))
    email = fields.String(required=require('email'))
    password = fields.String(required=require('password'))

    class Meta:
        fields = ('username', 'email', 'password', 'firstName', 'lastName')

    @validates_schema
    def validate_schema(self, data):

        username = data['username']
        existing_user = Users.query.filter_by(username_insensitive=username).first()
        if existing_user:
            raise ValidationError({'detail': "username '%s' already registered." % username, 'status': 409}, 'username')

        email = data['email']
        existing_user = Users.query.filter_by(email_insensitive=email).first()
        if existing_user:
            raise ValidationError({'detail': "email '%s' already registered." % email, 'status': 409}, 'email')

    @pre_load
    def unwrap_data(self, data):
        if 'data' in data:
            data = data['data']
        if 'attributes' in data:
            data = data['attributes']
        return data


user_post_serializer = UserPostSchema()
user_resource_serializer = UserResourceSchema()
