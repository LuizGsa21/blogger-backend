# -*- coding: utf-8 -*-
"""
    Unit Tests
    ~~~~~~~~~~
"""
import pprint

import unittest
import json
from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models import Users, Articles, Categories, Comments
from app.utils import Role
from flask.testing import FlaskClient
from flask import Response
from functools import wraps
import collections

# Patch the Flask client HTTP methods so we dont have to rollback after every request.
# Doing this ensures we aren't validating from uncommitted transactions.
# We can still use the original method by using `self.original_get`, `self.original_post` etc...
def rollback(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        response = func(*args, **kwargs)
        db.session.rollback()
        return response

    return decorator


for method_name in ('get', 'post', 'delete', 'patch', 'put'):
    old_method = getattr(FlaskClient, method_name)
    method = rollback(old_method)
    setattr(FlaskClient, 'original_' + method_name, old_method)
    setattr(FlaskClient, method_name, method)


def get_json(self):
    if not hasattr(self, '_json'):
        self._json = json.loads(self.data)
    return self._json


Response.get_json = get_json


class TestCase(unittest.TestCase):
    """Base TestCase for our application."""

    _RESOURCE_TYPES = {
        'users': Users,
        'articles': Articles,
        'comments': Comments,
        'categories': Categories
    }

    def setUp(self):
        """Reset all tables before testing."""
        self.app = create_app(config=TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        self.init_data()

    def tearDown(self):
        """Clean db session and drop all tables."""
        db.drop_all()
        self.ctx.pop()

    def init_data(self):
        session_add = db.session.add
        commit = db.session.commit
        all_categories = []
        for i, category in enumerate(('PHP', 'Python', 'C', 'C++', 'Java')):
            all_categories.append(Categories(name=category))
            session_add(all_categories[i])
        commit()
        all_users = []
        for i in range(10):
            all_users.append(Users(**{
                'username': 'bob%s' % i,
                'password': 'mypassword',
                'firstName': 'Jimmy%s' % i,
                'lastName': 'builder%s' % i,
            }))
            session_add(all_users[i])

        # create an admin user
        db.session.add(Users(**{
            'username': 'admin',
            'password': 'mypassword',
            'firstName': 'Mike',
            'lastName': 'Willy',
            'role': Role.ADMIN
        }))
        commit()
        user = all_users[0]
        category = all_categories[0]
        all_articles = []
        for i in range(3):
            article = Articles(**{
                'categoryId': category.id,
                'authorId': user.id,
                'title': 'Article #%s' % i,
                'body': 'Article body %s' % i,
            })
            all_articles.append(article)
            session_add(article)
        commit()
        article = all_articles[0]
        session_add(Comments(**{
            'parentId': None,
            'userId': 2,
            'articleId': article.id,
            'title': 'Comment #1',
            'body': 'nice article, you should write another!'
        }))
        session_add(Comments(**{
            'parentId': 1,
            'userId': 3,
            'articleId': article.id,
            'title': 'Replying to comment #1',
            'body': 'yeah I agree!'
        }))
        session_add(Comments(**{
            'parentId': 2,
            'userId': 4,
            'articleId': article.id,
            'title': 'Replying to comment #1',
            'body': 'yeah I agree!'
        }))

        commit()

    def login_with_id(self, id):
        user = Users.query.get(id)
        assert user
        return self.login(user.username, 'mypassword')

    def login(self, username, password):
        return self.client.post('/api/v1/auth/login',
                                data=json.dumps({'data': {'username': username, 'password': password}}),
                                content_type='application/json')

    def logout(self):
        return self.client.post('/api/v1/auth/logout', content_type='application/json')

    def login_as_admin(self):
        self.logout()
        response = self.login('admin', 'mypassword')
        self.assert_200_ok(response, 'Failed to login as admin.')

    def assert_status(self, response, status_code, message=None):
        message = message or 'HTTP Status %s expected but got %s' % (status_code, response.status_code)
        self.assertEqual(response.status_code, status_code, message)
        if status_code >= 400:
            data = response.get_json()
            assert 'errors' in data
            assert 'data' not in data
            assert len(data)

    def assert_200_ok(self, response, message=None):
        self.assert_status(response, 200, message)
        assert response.data, 'HTTP Status 200 but no body was found. Use 204 status instead.'

    def assert_201_created(self, response, message=None):
        self.assert_status(response, 201, message)

    def assert_204_no_content(self, response, message=None):
        self.assert_status(response, 204, message)
        assert response.data == '', 'HTTP Status 204 but response contains a body. Use 200 status instead.'

    def assert_400_bad_request(self, response, message=None):
        self.assert_status(response, 400, message)

    def assert_401_unauthorized(self, response, message=None):
        self.assert_status(response, 401, message)

    def assert_403_forbidden(self, response, message=None):
        self.assert_status(response, 403, message)

    def assert_404_not_found(self, response, message=None):
        self.assert_status(response, 404, message)

    def assert_405_method_not_allowed(self, response, message=None):
        self.assert_status(response, 405, message)

    def assert_409_conflict(self, response, message=None):
        self.assert_status(response, 409, message)

    def assert_500_internal_server_error(self, response, message=None):
        self.assert_status(response, 500, message)

    def assert_resource_response(self, response, type_, **kwargs):
        id_ = kwargs.get('id_', None)
        expected_count = kwargs.pop('expected_count', None)
        links = kwargs.get('links', None)

        if isinstance(response, Response):
            assert response.data  # expected non-empty response
            data = response.get_json()
            data = self.walk(data, 'data')
            if expected_count is not None:
                assert len(data) == expected_count
                if expected_count == 0:
                    return
            else:
                assert len(data)
        else:
            data = response

        if isinstance(data, list):
            if len(data) > 1:
                self.assert_resource_response(data[1:], type_, **kwargs)
            data = data[0]
        self._validate_type_and_id(data, type_, id_)
        self._validate_attributes(data, **kwargs)
        if links:
            self._validate_links(data, links)

    def _validate_type_and_id(self, data, type_, id_):
        # validate id and type
        assert type_ == self.walk(data, 'type')
        if id_ is not None:
            assert self.walk(data, 'id') == str(id_)
        else:
            assert self.walk(data, 'id') is not None

    def _validate_attributes(self, data, **kwargs):
        attributes_keys = kwargs.get('attributes_keys', [])
        attributes_exclude = kwargs.get('attributes_exclude', ())
        attributes_equal = kwargs.get('attributes_equal', {})
        attributes_not_equal = kwargs.get('attributes_not_equal', {})
        attributes_strict = kwargs.get('attributes_strict', False)

        # fetch resource attributes only if we are going to valid it.
        if attributes_exclude or attributes_equal or attributes_not_equal:
            r_attributes = self.walk(data, 'attributes')
            self.assertIsInstance(r_attributes, dict)
        else:
            r_attributes = {}

        # validate attributes
        if r_attributes:
            r_keys = r_attributes.keys()
            valid_keys = set(attributes_equal.keys() + attributes_not_equal.keys() + attributes_keys)
            if attributes_strict:
                assert len(valid_keys) == len(r_keys)
                assert (key in valid_keys for key in r_keys)
            for key, value in r_attributes.iteritems():
                if key in attributes_equal:
                    assert value == attributes_equal[key]
                elif key in attributes_not_equal:
                    assert value != attributes_equal[key]
            if attributes_exclude:
                keys_to_exclude = self.wrap_string(attributes_exclude)
                for key in keys_to_exclude:
                    assert key not in r_keys

    def _validate_links(self, data, links):
        # make it compatible
        links = self.wrap_string(links)
        r_links = self.walk(data, 'links')
        for key in links:
            assert key in r_links
            assert r_links[key]

    def walk(self, data, path, delimiter='.'):
        keys = path.split(delimiter, 1)
        key = keys[0]
        assert key in data
        if len(keys) > 1:
            return self.walk(data[key], keys[1], delimiter)
        else:
            return data[key]

    def wrap_string(self, string):
        if isinstance(string, str):
            return string,
        else:
            return string

    def assert_model(self, model, id_, attributes):
        obj = model.query.get(id_)
        assert obj
        for key, value in attributes.iteritems():
            assert getattr(obj, key) == value

    def assert_resource(self, resource, negate_attributes=False):
        resource = resource if 'data' not in resource else resource['data']
        obj = self.assert_resource_exists(resource)
        if 'attributes' in resource:
            for key, value in resource['attributes'].iteritems():
                if negate_attributes:
                    assert getattr(obj, key) != value
                else:
                    assert getattr(obj, key) == value

    def assert_resource_exists(self, resource):
        if 'data' in resource:
            resource = resource['data']
        model = self._RESOURCE_TYPES[resource['type']]
        assert model
        obj = model.query.get(resource['id'])
        assert obj
        return obj

    def assert_resource_should_not_exist(self, resource):
        if 'data' in resource:
            resource = resource['data']
        model = self._RESOURCE_TYPES[resource['type']]
        assert model
        obj = model.query.get(resource['id'])
        assert not obj

    def assert_resource_count(self, response, count):
        r = response.get_json()
        data = self.walk(r, 'data')
        assert len(data) == count

    def assert_resource_type(self, response, type_):
        r = response.get_json()
        data = self.walk(r, 'data')
        if isinstance(data, list):
            for obj in data:
                assert 'type' in obj
                assert obj['type'] == type_
