import pprint
from tests.base import TestCase
from app.models import Users, Articles
from app.extensions import db
import json
import pytest


class ResourceArticlesTestCase(TestCase):
    def test_get_articles(self):
        count = Articles.query.count()
        assert count  # verify fixture
        response = self.client.get('/api/v1/articles', content_type='application/json')
        self.assert_200_ok(response)
        self.assert_resource_count(response, count)

    def test_get_article_by_id(self):
        count = Articles.query.count()
        assert count > 2  # verify fixture

        response = self.client.get('/api/v1/articles/1', content_type='application/json')
        self.assert_200_ok(response)
        self.assert_resource_response(response,
                                      type_='articles',
                                      id_=1,
                                      attributes_keys=['title', 'body'],
                                      links='self')

    def test_put_article_by_id(self):
        resource = {
            'data': {
                'type': 'articles',
                'id': 1,
                'attributes': {
                    'title': 'New Title',
                    'body': 'New Body'
                }
            }
        }
        resource_json = json.dumps(resource)
        # attempt to update an article using an anonymous user. (This should fail)
        response = self.client.put('/api/v1/articles/1', data=resource_json, content_type='application/json')
        self.assert_401_unauthorized(response)
        self.assert_resource(resource, negate_attributes=True)

        # attempt to update an article using an registered who doesn't have ownership. (This should fail)
        self.login('bob1', 'mypassword')
        response = self.client.put('/api/v1/articles/1', data=resource_json, content_type='application/json')
        self.assert_403_forbidden(response)
        self.assert_resource(resource, negate_attributes=True)
        self.logout()

        # attempt to update an article using an registered who has ownership. (This should NOT fail)
        self.login_with_id(Articles.query.get(1).authorId)
        response = self.client.put('/api/v1/articles/1', data=resource_json, content_type='application/json')
        self.assert_204_no_content(response)
        self.assert_resource(resource)

    def test_post_articles(self):
        resource = {
            'data': {
                'type': 'articles',
                'attributes': {
                    'title': 'New Title',
                    'body': 'New Body'
                },
                'relationships': {
                    'category': {
                        'type': 'categories',
                        'id': '1'
                    }
                }
            }
        }
        resource_json = json.dumps(resource)
        # attempt to create an article using an anonymous user. (This should fail)
        response = self.client.post('/api/v1/articles', data=resource_json, content_type='application/json')
        self.assert_401_unauthorized(response)

        # create an article using a registered user. (This should NOT fail)
        self.login_with_id(1)
        response = self.client.post('/api/v1/articles', data=resource_json, content_type='application/json')
        self.assert_201_created(response)
        self.assert_resource_response(response,
                                      type_='articles',
                                      attributes_keys=['title', 'body'],
                                      links='self')
        id = response.get_json()['data']['id']
        resource['data']['id'] = id
        self.assert_resource(resource)

    def test_delete_article_by_id(self):
        resource = {
            'data': {
                'type': 'articles',
                'id': '2'
            }
        }
        resource_json = json.dumps(resource)

        # Anonymous users shouldn't be able to delete articles
        response = self.client.delete('/api/v1/articles/2', data=resource_json, content_type='application/json')
        self.assert_401_unauthorized(response)
        self.assert_resource_exists(resource)

        # attempt to delete an article using a registered user without ownership. (This should fail)
        self.login('bob3', 'mypassword')
        response = self.client.delete('/api/v1/articles/2', data=resource_json, content_type='application/json')
        self.assert_403_forbidden(response)
        self.assert_resource_exists(resource)
        self.logout()

        # finally, delete the article using the right user.
        self.login_with_id(Articles.query.get(2).authorId)
        response = self.client.delete('/api/v1/articles/2', data=resource_json, content_type='application/json')
        self.assert_204_no_content(response)
        self.assert_resource_should_not_exist(resource)
