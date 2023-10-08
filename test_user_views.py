"""User view tests."""

# run these tests like:
#
#    python -m unittest test_user_views.py


import os
import unittest
from models import db, connect_db, User, Message
from app import app, CURR_USER_KEY  # Import CURR_USER_KEY from your app

# Set the DATABASE_URL for testing
os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Create tables and set up the app for testing
db.create_all()
app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client and create test data."""
        db.drop_all()
        db.create_all()

        self.user = User.signup("testuser", "testuser@test.com", "password", None)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_logged_in_can_see_follower_following_pages(self):
        """When you're logged in, can you see the follower/following pages for any user?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.get(f"/users/{self.user.id}/followers")
            self.assertEqual(resp.status_code, 200)

            resp = c.get(f"/users/{self.user.id}/following")
            self.assertEqual(resp.status_code, 200)

def test_logged_out_cannot_see_follower_following_pages(self):
    """When you're logged out, are you disallowed from visiting a user's follower/following pages?"""

    resp = self.client.get(f"/users/{self.user.id}/followers", follow_redirects=False)
    self.assertEqual(resp.status_code, 302)
    self.assertEqual(resp.location, "http://localhost/login")

    resp = self.client.get(f"/users/{self.user.id}/following", follow_redirects=False)
    self.assertEqual(resp.status_code, 302)
    self.assertEqual(resp.location, "http://localhost/login")


    def test_logged_in_can_add_message(self):
        """When you're logged in, can you add a message as yourself?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.post("/messages/new", data={"text": "Test message"})
            self.assertEqual(resp.status_code, 302)

            message = Message.query.one()
            self.assertEqual(message.text, "Test message")
            self.assertEqual(message.user_id, self.user.id)

    def test_logged_in_can_delete_message(self):
        """When you're logged in, can you delete a message as yourself?"""

        message = Message(text="Test message", user_id=self.user.id)
        db.session.add(message)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            resp = c.post(f"/messages/{message.id}/delete")
            self.assertEqual(resp.status_code, 302)

            deleted_message = Message.query.get(message.id)
            self.assertIsNone(deleted_message)

if __name__ == '__main__':
    unittest.main()

