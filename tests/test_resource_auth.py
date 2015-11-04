from tests.base import TestCase
import json


class ResourceAuthTestCase(TestCase):
    def test_login_and_logout_endpoints(self):
        # Login user
        response = self.login('bob1', 'universe1')
        self.assert_200_ok(response)
        self.assert_resource_response(response, type_='users',
                                      id_=2,
                                      attributes_equal={'username': 'bob1'})

        # Login again without login out, we should get a 400 status code
        response = self.login('bob1', 'universe1')
        self.assert_400_bad_request(response)
        assert 'You are already login as bob1' in response.data

        # Logout user
        response = self.client.post('/api/v1/auth/logout', content_type='application/json')
        self.assert_200_ok(response)

        # Logout again, we should get a 400 status code because we are not logged in
        response = self.client.post('/api/v1/auth/logout', content_type='application/json')
        self.assert_400_bad_request(response)
        assert 'You are not logged in.' in response.data

