from .users import (
    UserSchema,
    UserPostSchema
)


user_serializer = UserSchema()
users_serializer = UserSchema(many=True)

user_post_serializer = UserPostSchema()
