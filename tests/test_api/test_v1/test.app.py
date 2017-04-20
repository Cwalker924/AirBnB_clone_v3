import unittest
from api.v1.app import app
from flask import Flask
from flask import jsonify
from flask import request


class Test_API_v1(unittest.TestCase):
    """
    Test main Flask route handlers Cred. Philip Yoo & Walton Lee test suite
    """
    def setUp(self):
        self.app = app.test_client(self)
        self.app.testing = True

    def tearDown(self):
        self.app.testing = False

    def test_not_found_status(self):
        result = self.app.get('/non-existant-route')
        self.assertEqual(result.status_code, 404)
        self.assertEqual(result.status, "404 NOT FOUND")

    def test_not_found_return(self):
        result = self.app.get('/non-existant-route')
        self.assertEqual(result.headers['Content-Type'], 'application/json')


if __name__ == "__main__":
    unittest.main()
    Contact GitHub API Training Shop Blog About
