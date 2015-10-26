import pprint
from tests import TestCase
from app.models import Users
from app.extensions import db
import json


class TestUserResource(TestCase):
    def test_create_user(self):
        newUser = {
            'username': 'LuizGsa21',
            'email': 'LuizGsa21@email.com',
            'firstName': 'Luiz',
            'lastName': 'Arantes Sa',
            'password': 'password-123',
            'isAdmin': 1
        }
        old_count = Users.query.count()
        # create a new user
        response = self.client.post('/api/v1/users', data=json.dumps(newUser), content_type='application/json')
        db.session.rollback()
        self.assertEqual(old_count, Users.query.count() - 1, 'Expected a user to be created.')
        self.assertEqual(response.status_code, 201,
                         'Received %s Expected 201 status for when a resource is created.' % response.status)
        self.assertFalse('password' in response.data, 'Password should not be returned in response.')

        # create a user using the same credentials. This should fail and return a 409 status.
        response = self.client.post('/api/v1/users', data=json.dumps(newUser), content_type='application/json')
        db.session.rollback()
        self.assertEqual(response.status_code, 409, 'Expected 409 status since resource already exists.')
        self.assertEqual(old_count, Users.query.count() - 1, "A user shouldn't have been created.")

    def test_get_users(self):
        response = self.client.get('/api/v1/users', content_type='application/json')
        assert response.data, 'Expected a non-empty response'
        data = response.data
        assert 'password' not in data, 'Password field should not be returned'
        data = json.loads(data)
        assert Users.query.count() == len(data['data']), 'Expected all users to be returned'

    def test_get_user_by_id(self):
        response = self.client.get('/api/v1/users/2', content_type='application/json')
        assert response.data, 'Expected a non-empty response'
        data = response.data
        assert 'password' not in data, 'Password field should not be returned'
        data = json.loads(data)
        assert data['data']['id'] == 2
        assert data['data']['type'] == 'users'
        attributes = data['data']['attributes']
        assert attributes['username'] == 'bob1', \
            'Expected user name to be `{0}` but got `{1}`'.format('bob1', attributes['username'])

    def test_delete_user_by_id(self):
        user = Users.query.get(2)
        assert user, 'Failed to load fixture. User missing...'
        response = self.client.delete('/api/v1/users/2', content_type='application/json')
        db.session.rollback()
        assert response.status_code == 200, 'Expected 200 response but got %s instead.' % response.status_code
        assert response.data, 'Expected a non-empty response'
        data = json.loads(response.data)
        assert data['data'] is None, 'Expected data attribute to be none.'
        assert Users.query.get(2) is None, 'Expected user with id 2 to be deleted.'

