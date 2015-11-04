from marshmallow import validates_schema, validates, ValidationError
from app.models import Users
from .base import ResourceSchema, fields, Schema
from app.utils import Role, Method


class ResourceUserSchema(ResourceSchema):
    class Meta:
        type = 'users'


class UserSchema(Schema):
    username = fields.String()
    dateJoined = fields.DateTime()
    password = fields.String(load_only=True)

    class Meta:
        fields = Users.get_admin_safe_keys(Method.CREATE)

    @validates('email')
    def validate_email(self, email):
        existing_user = Users.query.filter_by(email_insensitive=email).first()
        if existing_user:
            raise ValidationError({'detail': "email '%s' already registered." % email, 'status': 409})

    @validates('username')
    def validate_username(self, username):
        existing_user = Users.query.filter_by(username_insensitive=username).first()
        if existing_user:
            raise ValidationError({'detail': "username '%s' already registered." % username, 'status': 409})

    @validates_schema(pass_original=True)
    def validate_schema(self, data, original):
        self.validate_permission(data, original)


class UserCreateSchema(UserSchema):
    username = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

    class Meta:
        fields = Users.get_admin_safe_keys(Method.CREATE)


create_user_admin_serializer = ResourceUserSchema(
    UserCreateSchema
)
edit_user_admin_serializer = ResourceUserSchema(
    UserSchema
)

create_user_serializer = ResourceUserSchema(
    UserCreateSchema, param={'only': Users.get_safe_columns(Method.CREATE, Role.GUEST)}
)

edit_user_profile_serializer = ResourceUserSchema(
    UserSchema, param={'only': Users.get_safe_columns(Method.UPDATE, Role.USER)}
)

view_user_serializer = ResourceUserSchema(
    UserSchema, param={'only': Users.get_safe_columns(Method.READ, Role.GUEST)}
)
