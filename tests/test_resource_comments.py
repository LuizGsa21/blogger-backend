import pprint
from tests.base import TestCase
from app.models import Users, Comments
from app.extensions import db
import json
import pytest


class ResourceCommentsTestCase(TestCase):
    def test_get_comments(self):
        count = Comments.query.count()
        assert count  # verify fixture
        response = self.client.get('/api/v1/comments', content_type='application/json')
        self.assert_200_ok(response)
        self.assert_resource_count(response, count)

    def test_get_comment_by_id(self):
        count = Comments.query.count()
        assert count > 2  # verify fixture

        response = self.client.get('/api/v1/comments/1', content_type='application/json')
        self.assert_200_ok(response)
        self.assert_resource_response(response,
                                      type_='comments',
                                      id_=1,
                                      attributes_keys=['title', 'body', 'lastModified', 'dateCreated'],
                                      attributes_exclude=['parentId', 'userId', 'articleId'],
                                      links='self')

