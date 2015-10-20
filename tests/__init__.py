# -*- coding: utf-8 -*-
"""
    Unit Tests
    ~~~~~~~~~~
"""

import unittest
from app import create_app
from app.config import TestConfig
from app.extensions import db
from app.model import Users


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
        db.session.commit()
