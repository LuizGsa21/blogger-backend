from marshmallow import Schema, fields, validates_schema, ValidationError
from app.models import Users
from .schema_helpers import require


class UserSchema(Schema):
    class Meta:
        fields = ('username', 'firstName', 'lastName', 'dateJoined', 'avatarPath')


class UserResourceSchema(Schema):
    type = fields.String('users')
    id = fields.Function(lambda obj: obj.id)
    attributes = fields.Function(lambda obj: user_serializer.dump(obj).data)
    links = fields.Function(lambda obj: {'self': obj.url})


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


user_serializer = UserSchema()
user_post_serializer = UserPostSchema()
user_resource_serializer = UserResourceSchema()
