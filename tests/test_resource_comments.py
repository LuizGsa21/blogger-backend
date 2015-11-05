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

