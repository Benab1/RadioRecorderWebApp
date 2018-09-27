from app import app, models, db
from datetime import datetime
import unittest
import flask_testing
from flask import Flask, request
from flask_testing import TestCase
from flask_login import LoginManager, current_user, AnonymousUserMixin
from app.models import Account, Recordings

""" Firstly you need to pip install flask-testing then add to requirements.
   
    Then uncomment the test configuration stuff in the config file.
    then to run go into the webapp directory and enter python test.py


"""


class BaseTestCase(TestCase):

    # Configures the app to a flask-testing supported configuration
    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    # Create all the tables and destroy them with each unit test to ensure
    # they're clean and self contained.
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class FlaskTestCase(BaseTestCase):

    # Functions to reduce repeated code in test suite.

    # Function to speed up login requests
    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    # Function to speed up log out requests
    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    # Function to quickly register user for further use.
    def register(self, username, password):
        return self.client.post(
            '/register',
            data=dict(username=username, password=password),
            follow_redirects=True)

#---------------------------webapp endpoint testing-----------------------------#
    # Test home route redirects to login page, this indicates the home page is not accessible
    # unless you are logged in, here we test that the appropriate 302 HTML response code for a redirect
    # is registered.
    def test_home_redirects(self):
        response = self.client.get('/home', content_type='html/text')
        self.assertEqual(response.status_code, 302)

    # ensure login page loads
    def test_login_page_loads(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertTrue(b'Log In' in response.data)

    # ensure sign_up page loads
    def test_registration_page_loads(self):
        response = self.client.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # ensure order ticket page loads
    def test_recordings_page_requires_login(self):
        response = self.client.get(
            '/recordings', content_type='html/text', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    # Ensure that logout page requires user login, this is confirmed by the
    # flashing of the
    def test_logout_route_requires_login(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Please log in to access this page', response.data)

# #-----------------------Form Validation---------------------------------------#

    # ensure login works with correct account
    def test_working_login(self):
        self.register('ben', 'password')
        with self.client:
            response = self.client.post(
                '/login', data=dict(username='ben', password='password'),
                follow_redirects=True)
            self.assertIn(b'Logged in successfully', response.data)

    # Ensure one User can only be registed once
    def test_user_registration_duplicate_email(self):
        response = self.register(
            'ben', '123')
        self.assertEqual(response.status_code, 200)
        response = self.register(
            'ben', '1234')
        self.assertIn(
            b'User ben is already  registered.',
            response.data)

    # Test successful validation of record form.
    def test_record_form(self):
        self.register('ben', '123')
        self.login('ben', '123')
        with self.client:
            response = self.client.post(
                '/record', data=dict(instream='NPR', Year=2018, Month=9,
                                     Day=7, Hour=17, Minutes=10, Seconds=0, file_name='Form Test',
                                     duration='00:02:00'), follow_redirects=True)
            self.assertIn(b'Form Test', response.data)


if __name__ == '__main__':
    unittest.main()
