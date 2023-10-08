"""Message Model tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_model.py


import os
import unittest
from models import db, connect_db, User
from app import app

# Set the DATABASE_URL for testing
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Create tables and set up the app for testing
db.create_all()
app.config['WTF_CSRF_ENABLED'] = False

class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and create test data."""
        db.drop_all()
        db.create_all()

        # Create test users
        self.user1 = User.signup("user1", "user1@test.com", "password1", None)
        self.user2 = User.signup("user2", "user2@test.com", "password2", None)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""

        self.user1.following.append(self.user2)
        db.session.commit()

        self.assertTrue(self.user1.is_following(self.user2))
        self.assertFalse(self.user2.is_following(self.user1))  # user2 is not following user1

    def test_is_not_following(self):
        """Does is_following successfully detect when user1 is not following user2?"""

        self.assertFalse(self.user1.is_following(self.user2))
        self.assertFalse(self.user2.is_following(self.user1))

    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""

        self.user2.following.append(self.user1)
        db.session.commit()

        self.assertTrue(self.user1.is_followed_by(self.user2))
        self.assertFalse(self.user2.is_followed_by(self.user1))  # user2 is not followed by user1

    def test_is_not_followed_by(self):
        """Does is_followed_by successfully detect when user1 is not followed by user2?"""

        self.assertFalse(self.user1.is_followed_by(self.user2))
        self.assertFalse(self.user2.is_followed_by(self.user1))

if __name__ == '__main__':
    unittest.main()
