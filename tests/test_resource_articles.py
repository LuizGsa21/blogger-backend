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

    # def test_get_articles_by_id(self):
    #     pass
    #
    # def test_put_article_by_id(self):
    #     pass
    #
    # def test_post_articles(self):
    #     pass
    #
    # def test_delete_article_by_id(self):
    #     pass
