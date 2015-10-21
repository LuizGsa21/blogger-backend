from tests import TestCase
from app.models import Users
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
        userCount = Users.query.count()
        # create a new user
        response = self.client.post('/api/v1/users', data=json.dumps(newUser), content_type='application/json')
        self.assertEqual(userCount, Users.query.count() - 1, 'Expected a user to be created.')
        self.assertEqual(response.status_code, 201,
                         'Received %s Expected 201 status for when a resource is created.' % response.status)
        self.assertFalse('password' in response.data, 'Password should not be returned in response.')

        # create a user using the same credentials. This should fail and return a 409 status.
        response = self.client.post('/api/v1/users', data=json.dumps(newUser), content_type='application/json')
        self.assertEqual(response.status_code, 409, 'Expected 409 status since resource already exists.')
