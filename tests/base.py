# -*- coding: utf-8 -*-
"""
    Unit Tests
    ~~~~~~~~~~
"""

import unittest
from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.models import Users, Articles, Categories


class TestCase(unittest.TestCase):
    """Base TestClass for your application."""

    def setUp(self):
        """Reset all tables before testing."""
        self.app = create_app(config=TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        self.init_data()

    def tearDown(self):
        """Clean db session and drop all tables."""
        db.drop_all()
        self.ctx.pop()

    def init_data(self):
        session_add = db.session.add
        all_categories = []
        for i, category in enumerate(('PHP', 'Python', 'C', 'C++', 'Java')):
            all_categories.append(Categories(name=category))
            session_add(all_categories[i])

        all_users = []
        for i in range(10):
            all_users.append(Users(**{
                'username': 'bob%s' % i,
                'password': 'universe%s' % i,
                'firstName': 'Jimmy%s' % i,
                'lastName': 'builder%s' % i,
            }))
            session_add(all_users[i])

        user = all_users[0]
        category = all_categories[0]
        # for i in range(5):
        Articles(**{
            'categoryId': category.id,
            'authorId': user.id,
            'title': 'Article #%s',
            'body': 'Article body %s',
        })
        db.session.commit()
