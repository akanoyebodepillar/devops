import unittest
from flask import Flask
from flask_testing import TestCase
import json

# Import your Flask app
from app import app, users

class MyTest(TestCase):

    def create_app(self):
        # Configure your app for testing
        app.config['TESTING'] = True
        return app

    def setUp(self):
        # This method is called before each test
        self.client = self.app.test_client()

    def tearDown(self):
        # This method is called after each test
        pass

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, World!", response.data)

    def test_get_users(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), len(users))

    def test_add_user(self):
        new_user = {'name': 'Charlie'}
        response = self.client.post('/users', data=new_user)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Charlie')

    def test_get_user_by_id(self):
        response = self.client.get('/users/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Alice')

        response = self.client.get('/users/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'User not found')

if __name__ == '__main__':
    unittest.main()