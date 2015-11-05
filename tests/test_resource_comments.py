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

    def test_put_comment_by_id(self):
        resource = {
            'data': {
                'type': 'comments',
                'id': 1,
                'attributes': {
                    'title': 'New Title',
                    'body': 'New Body'
                }
            }
        }
        resource_json = json.dumps(resource)
        comment = Comments.query.get(1)

        # attempt to update an comment using an anonymous user. (This should fail)
        response = self.client.put('/api/v1/comments/1', data=resource_json, content_type='application/json')
        self.assert_401_unauthorized(response)
        self.assert_resource(resource, negate_attributes=True)

        # attempt to update an comment using an registered who doesn't have ownership. (This should fail)
        self.login_with_id(comment.userId + 1)
        response = self.client.put('/api/v1/comments/1', data=resource_json, content_type='application/json')
        self.assert_403_forbidden(response)
        self.assert_resource(resource, negate_attributes=True)
        self.logout()

        # attempt to update an comment using an registered who has ownership. (This should NOT fail)
        self.login_with_id(comment.userId)
        response = self.client.put('/api/v1/comments/1', data=resource_json, content_type='application/json')
        self.assert_204_no_content(response)
        self.assert_resource(resource)

