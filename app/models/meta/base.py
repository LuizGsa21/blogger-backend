import pprint
from app.extensions import db
from datetime import datetime
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin, current_user
from app.utils import Role, Method
from sqlalchemy.orm import Load, load_only
from sqlalchemy.sql.expression import literal_column


def _relationships(self):
    raise NotImplemented


def get_columns(cls, method, role):
    if role == Role.ADMIN:
        return cls.get_admin_columns(method)
    elif role == Role.USER:
        return cls.get_user_columns(method)
    elif role == Role.GUEST:
        return cls.get_guest_columns(method)
    else:
        raise RuntimeError('Unknown role: {}'.format(role))


def get_admin_columns(cls, method):
    return tuple(cls.__mapper__.columns.keys())


def get_guest_columns(cls, method):
    raise NotImplemented


def get_user_columns(cls, method):
    raise NotImplemented


def get_relationships(self, only=(), included=False):
    if only:
        resources = only
    else:
        resources = self._relationships
    if included:
        included_data = []
        relationships = {resource: self.get_relationship(resource, included_data=included_data) for resource in resources}
        return relationships, included_data
    return {resource: self.get_relationship(resource) for resource in resources}


def to_resource(self, columns):
    return {
        'id': self.id,
        'type': self.__tablename__,
        'attributes': {column: getattr(self, column) for column in columns if hasattr(self, column)}
    }
    pass


def get_relationship(self, type_, included_data=None):
    items = getattr(self, type_)

    if not isinstance(items, db.Model):
        items = items.options(load_only('id')).all()
        results = []
        if items:
            columns = items[0].get_columns(Method.READ, Role.ADMIN)
            for item in items:
                results.append({'id': item.id, 'type': type_})
                if included_data is not None:
                    included_data.append(item.to_resource(columns))
    else:
        item = items
        results = {'id': item.id, 'type': type_}
        if included_data is not None:
            included_data.append(item.to_resource(item.get_columns(Method.READ, Role.ADMIN)))
    data = {
        'links': {
            'related': url_for(type_ + '.get_' + type_, _external=True)
        },
        'data': results
    }
    return data

# Extending db.Model as a base class throws an InvalidRequestError exception
# so for now just patch the methods dynamically
db.Model.get_columns = classmethod(get_columns)
db.Model.get_admin_columns = classmethod(get_admin_columns)
db.Model.get_guest_columns = classmethod(get_guest_columns)
db.Model.get_user_columns = classmethod(get_user_columns)
db.Model._relationships = _relationships
db.Model.get_relationships = get_relationships
db.Model.get_relationship = get_relationship
db.Model.to_resource = to_resource
