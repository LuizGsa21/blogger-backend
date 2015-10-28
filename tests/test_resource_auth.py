from tests.base import TestCase
import json


class ResourceAuthTestCase(TestCase):
    def test_login_and_logout_endpoints(self):
        # Login user
        response = self.login('bob1', 'universe1')
        assert response.status_code == 200
        assert response.data
        data = json.loads(response.data)['data']['attributes']
        assert data['username'] == 'bob1'

        # Login again without login out, we should get a 400 status code
        response = self.login('bob1', 'universe1')
        assert response.status_code == 400
        assert 'You are already login as bob1' in response.data

        # Logout user
        response = self.client.post('/api/v1/auth/logout', content_type='application/json')
        assert response.status_code == 200

        # Logout again, we should get a 400 status code because we are not logged in
        response = self.client.post('/api/v1/auth/logout', content_type='application/json')
        assert response.status_code == 400
        assert 'You are not logged in.' in response.data

