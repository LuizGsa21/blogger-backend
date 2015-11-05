import pprint
from tests.base import TestCase
from app.models import Users, Categories
from app.extensions import db
import json
from app.utils import Role


class ResourceUsersTestCase(TestCase):
    def _get_post_categories_fixture(self):
        return {
            'data': {
                'type': 'categories',
                'attributes': {
                    'name': 'NEW CATEGORY',
                }
            }
        }

    def test_only_admin_can_access_post_put_delete_endpoints(self):
        # attempt as an anonymous user
        response = self.client.put('/api/v1/categories/1')
        self.assert_401_unauthorized(response)
        response = self.client.post('/api/v1/categories')
        self.assert_401_unauthorized(response)
        response = self.client.delete('/api/v1/categories/1')
        self.assert_401_unauthorized(response)

        # attempt as a registered
        self.login_with_id(1)
        response = self.client.put('/api/v1/categories/1')
        self.assert_403_forbidden(response)
        response = self.client.post('/api/v1/categories')
        self.assert_403_forbidden(response)
        response = self.client.delete('/api/v1/categories/1')
        self.assert_403_forbidden(response)
        self.logout()

    def test_post_categories(self):
        self.login_as_admin()
        new_resource = self._get_post_categories_fixture()
        response = self.client.post('/api/v1/categories', data=json.dumps(new_resource))
        self.assert_201_created(response)
        self.assert_resource_response(response,
                                      type_='categories',
                                      links='self')

    def test_get_categories(self):
        current_count = Categories.query.count()
        response = self.client.get('/api/v1/categories')
        self.assert_200_ok(response)
        self.assert_resource_count(response, current_count)
        self.assert_resource_type(response, 'categories')

    def test_get_category_by_id(self):
        pass

    def test_delete_category_by_id(self):
        pass

    def test_put_category_by_id(self):
        pass

    def test_patch_category_by_id(self):
        pass
