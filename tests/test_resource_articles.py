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
        assert response.data  # expect a non-empty response
        data = json.loads(response.data)
        assert len(data['data']) == count  # expect all articles to be returned

        article = data['data'][0]
        assert article['type'] == 'articles'
        assert 'id' in article
        assert 'id' not in article['attributes']
        assert len(article['attributes']['title'])
        assert len(article['attributes']['body'])

    def test_get_article_by_id(self):
        count = Articles.query.count()
        assert count > 2  # verify fixture

        response = self.client.get('/api/v1/articles/2', content_type='application/json')
        assert response.data  # expect a non-empty response
        data = json.loads(response.data)

        article = data['data']
        assert article['type'] == 'articles'
        assert 'id' in article
        assert 'id' not in article['attributes']
        assert len(article['attributes']['title'])
        assert len(article['attributes']['body'])

    def test_put_article_by_id(self):
        updated_fields = {
            'data': {
                'type': 'articles',
                'id': 1,
                'attributes': {
                    'title': 'New Title',
                    'body': 'New Body'
                }
            }
        }
        response = self.client.put('/api/v1/articles/1', data=json.dumps(updated_fields), content_type='application/json')
        assert response.data  # expect a non-empty response
        assert response.status_code == 200
        data = json.loads(response.data)['data']['attributes']
        fields = updated_fields['data']['attributes']
        assert data['title'] == fields['title']
        assert data['body'] == fields['body']

    # def test_post_articles(self):
    #     new_article = {
    #         'data': {
    #             'type': 'articles',
    #             'attributes': {
    #                 'title': 'New Title',
    #                 'body': 'New Body'
    #             }
    #         }
    #     }
    #     old_count = Articles.query.count()
    #     assert old_count  # verify fixture
    #     response = self.client.post('/api/v1/articles', data=json.dumps(new_article), content_type='application/json')
    #
    #     assert response.data  # expect a non-empty response
    #     assert response.status_code == 200
    #
    #     data = json.loads(response.data)['data']
    #     assert data['links']['self']  # expect a url referencing the new resource
    #
    #     attributes = new_article['data']['attributes']
    #     data = data['attributes']
    #     assert data['title'] == attributes['title']
    #     assert data['body'] == attributes['body']

    # def test_delete_article_by_id(self):
    #
    #     # Anonymous users shouldn't be able to delete articles
    #     response = self.client.delete('/api/v1/articles/2', content_type='application/json')
    #     assert response.status_code == 403
    #     assert Articles.query.get(2)
    #
    #     self.login('bob3', 'universe3')
    #     # Even though we are logged in, we shouldn't be able to delete articles from other users
    #     response = self.client.delete('/api/v1/articles/2', content_type='application/json')
    #     assert response.status_code == 403  # we should have permission
    #     assert Articles.query.get(2)
    #
    #     self.logout()
    #     self.login('bob1', 'universe1')
    #     assert Articles.query.get(3).authorId == 1  # verify fixture
    #
    #     # now we should be able to delete the article
    #     response = self.client.delete('/api/v1/articles/3', content_type='application/json')
    #     assert response.status_code == 200
    #     data = json.loads(response.data)
    #     assert data['data'] is None
    #     assert Articles.query.get(3) is None  # article should be deleted
