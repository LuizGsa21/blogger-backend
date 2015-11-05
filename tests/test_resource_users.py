import pprint
from tests.base import TestCase
from app.models import Users
from app.extensions import db
import json
from app.utils import Role


class ResourceUsersTestCase(TestCase):
    def _get_post_users_fixture(self):
        return {
            'data': {
                'type': 'users',
                'attributes': {
                    'username': 'LuizGsa21',
                    'email': 'LuizGsa21@email.com',
                    'firstName': 'Luiz',
                    'lastName': 'Arantes Sa',
                    'password': 'password-123'
                }
            }
        }

    def test_post_users(self):
        new_user = self._get_post_users_fixture()
        # ensure user doesn't exist
        get_user = Users.query.filter_by(username='LuizGsa21')
        assert get_user.first() is None

        response = self.client.post('/api/v1/users', data=json.dumps(new_user), content_type='application/json')
        self.assert_201_created(response)
        self.assert_resource_response(response,
                                      type_='users',
                                      links='self',
                                      attributes_exclude='password')
        assert get_user.first()  # expect the created user
        # create a user using the same credentials. This should fail and return a 409 status.
        response = self.client.post('/api/v1/users', data=json.dumps(new_user), content_type='application/json')
        self.assert_409_conflict(response)
        assert get_user.count() == 1

    def test_admin_post_users(self):
        new_user = self._get_post_users_fixture()
        new_user['data']['attributes']['role'] = Role.ADMIN

        # ensure user doesn't exist
        get_user = Users.query.filter_by(username='LuizGsa21')
        assert get_user.first() is None

        # create an admin user (This should fail, we can only create an admin if we are logged in as admin)
        response = self.client.post('/api/v1/users', data=json.dumps(new_user), content_type='application/json')
        self.assert_403_forbidden(response)
        assert get_user.first() is None

        # login as admin and create an admin user
        self.login_as_admin()
        response = self.client.post('/api/v1/users', data=json.dumps(new_user), content_type='application/json')
        self.assert_201_created(response)
        self.assert_resource_response(response,
                                      type_='users',
                                      links='self',
                                      attributes_exclude='password')
        assert get_user.first()  # expected a user to be created
        self.logout()

    def test_get_users(self):
        response = self.client.get('/api/v1/users', content_type='application/json')
        self.assert_200_ok(response)
        self.assert_resource_response(response,
                                      type_='users',
                                      links='self',
                                      attributes_keys=['username', 'lastName', 'avatarPath', 'dateJoined', 'firstName'],
                                      attributes_exclude='password',
                                      expected_count=Users.query.count())

    def test_get_user_by_id(self):
        response = self.client.get('/api/v1/users/1', content_type='application/json')
        self.assert_200_ok(response)
        self.assert_resource_response(response,
                                      type_='users',
                                      id_=1,
                                      links='self',
                                      attributes_equal={'username': 'bob0'},
                                      attributes_exclude='password')

    def test_delete_user_by_id(self):
        # attempt to delete a user using an anonymous user. Note: this should fail
        response = self.client.delete('/api/v1/users/2', content_type='application/json')
        self.assert_401_unauthorized(response)
        assert Users.query.get(2)

        # attempt to delete a user using an registered user. Note: this should fail
        self.login('bob1', 'mypassword')
        response = self.client.delete('/api/v1/users/2', content_type='application/json')
        self.assert_403_forbidden(response)
        assert Users.query.get(2)
        self.logout()

        # attempt to delete a user as an admin.
        self.login_as_admin()
        response = self.client.delete('/api/v1/users/2', content_type='application/json')
        self.assert_204_no_content(response)
        assert Users.query.get(2) is None

    def test_put_user_by_id(self):
        resource = {
            'data': {
                'type': 'users',
                'id': "2",
                'attributes': {
                    'username': 'LuizGsa21',
                    'email': 'LuizGsa21@email.com',
                    'firstName': 'Luiz',
                    'lastName': 'Arantes Sa',
                    'oauthProvider': 'google-plus',
                    'oauthId': '10293985777388',
                    'avatarPath': 'avatar_new.jpg',
                    'role': Role.ADMIN
                }
            }
        }
        resource_json = json.dumps(resource)
        # attempt to update a user using an anonymous user. (This should fail)
        response = self.client.put('/api/v1/users/2', data=resource_json, content_type='application/json')
        self.assert_401_unauthorized(response)
        self.assert_resource(resource, negate_attributes=True)

        # attempt to update a user using an registered user. (This should fail)
        self.login('bob1', 'mypassword')
        response = self.client.put('/api/v1/users/2', data=resource_json, content_type='application/json')
        self.assert_403_forbidden(response)
        self.assert_resource(resource, negate_attributes=True)
        self.logout()

        # attempt to update a user as an admin. (This should NOT fail)
        self.login_as_admin()
        response = self.client.put('/api/v1/users/2', data=resource_json, content_type='application/json')
        self.assert_204_no_content(response)
        self.assert_resource(resource)

    def test_patch_user_by_id(self):
        resource = {
            'data': {
                'type': 'users',
                'id': "2",
                'attributes': {
                    'email': 'LuizGsa21@email.com',
                    'firstName': 'Luiz',
                    'lastName': 'Arantes Sa',
                    'avatarPath': 'avatar_new.jpg',
                }
            }
        }
        resource_json = json.dumps(resource)
        # attempt to update a user using an anonymous user. (This should fail)
        response = self.client.patch('/api/v1/users/2', data=resource_json, content_type='application/json')
        self.assert_401_unauthorized(response)
        self.assert_resource(resource, negate_attributes=True)

        # attempt to update a user using an registered user who's id doesn't match (This should fail)
        self.login('bob0', 'mypassword')
        response = self.client.patch('/api/v1/users/2', data=resource_json, content_type='application/json')
        self.assert_403_forbidden(response)
        self.assert_resource(resource, negate_attributes=True)
        self.logout()

        # attempt to update a user using an registered whos id matches (This should NOT fail)
        self.login('bob1', 'mypassword')
        response = self.client.patch('/api/v1/users/2', data=resource_json, content_type='application/json')
        self.assert_204_no_content(response)
        self.assert_resource(resource)

