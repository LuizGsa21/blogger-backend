import pprint
from tests.base import TestCase
from app.models import Users
from app.extensions import db
import json


class ResourceUsersTestCase(TestCase):
    def test_post_users(self):
        new_user = {
            'data': {
                'type': 'users',
                'attributes': {
                    'username': 'LuizGsa21',
                    'email': 'LuizGsa21@email.com',
                    'firstName': 'Luiz',
                    'lastName': 'Arantes Sa',
                    'password': 'password-123',
                    'isAdmin': 1
                }
            }
        }
        old_count = Users.query.count()
        # create a new user
        response = self.client.post('/api/v1/users', data=json.dumps(new_user), content_type='application/json')
        db.session.rollback()
        assert response.status_code == 201  # expected 201 status when a resource is created
        assert response.data
        assert old_count + 1 == Users.query.count()  # a new user should have been created
        data = json.loads(response.data)['data']
        assert data['links']['self']  # expected a self link to access the created resource

        # create a user using the same credentials. This should fail and return a 409 status.
        response = self.client.post('/api/v1/users', data=json.dumps(new_user), content_type='application/json')
        db.session.rollback()
        assert response.status_code == 409
        assert response.data
        assert old_count + 1 == Users.query.count()  # count should still be the same

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

        # attempt to delete a user using an anonymous user. Note: this should fail
        response = self.client.delete('/api/v1/users/2', content_type='application/json')
        db.session.rollback()
        assert response.status_code == 403
        assert response.data
        data = json.loads(response.data)
        assert data['errors']
        assert Users.query.get(2)

        # attempt to delete a user using an registered user. Note: this should fail
        self.login('bob1', 'universe1')
        response = self.client.delete('/api/v1/users/2', content_type='application/json')
        db.session.rollback()
        assert response.status_code == 403
        assert response.data
        data = json.loads(response.data)
        assert data['errors']
        assert Users.query.get(2)
        self.logout()

        # attempt to delete a user as an admin.
        self.login('bob0', 'universe0')
        user = Users.query.filter_by(username='bob0').first()
        user.isAdmin = True
        db.session.commit()
        response = self.client.delete('/api/v1/users/2', content_type='application/json')
        db.session.rollback()
        assert response.data
        data = json.loads(response.data)
        assert data['data'] is None
        assert Users.query.get(2) is None

    def test_put_user_by_id(self):
        updated_fields = {
            'data': {
                'type': 'users',
                'id': 1,
                'attributes': {
                    'username': 'LuizGsa21',
                    'email': 'LuizGsa21@email.com',
                    'firstName': 'Luiz',
                    'lastName': 'Arantes Sa',
                    'avatarPath': 'avatar.jpg',
                    'isAdmin': 1
                }
            }
        }
        response = self.client.put('/api/v1/users/1', data=json.dumps(updated_fields), content_type='application/json')
        assert response.data, 'Expected a non-empty response'
        db.session.rollback()
        assert response.status_code == 200, 'Expected 200 response but got %s instead.' % response.status_code
        assert response.data, 'Expected a non-empty response'
        data = json.loads(response.data)['data']['attributes']
        fields = updated_fields['data']['attributes']
        assert data['username'] == fields['username'], 'Failed to update `username`'
        assert data['firstName'] == fields['firstName'], 'Failed to update `firstName`'
        user = Users.query.get(1)
        assert user.isAdmin == 0,\
            'We should not be able to update admin fields when using the endpoint api'

