#!/usr/bin/env python3

import server

import json
import os
import requests
import tempfile
import unittest

class TestUser(unittest.TestCase):
    def is_user(self, data):
        self.assertTrue('email' in data)
        self.assertEqual(self.user['email'], data['email'])

        self.assertTrue('name' in data)
        self.assertEqual(self.user['name'], data['name'])

    def setUp(self):
        self.app = server.app.test_client()
        self.db, server.app.config['DATABASE'] = tempfile.mkstemp()
        self.user = {"email": "testing@bendoan.me",
                "name": "Ben doan",
                "password": "password"}

    def test_add(self):
        r = self.app.post("/user/add", data=self.user)
        data = json.loads(r.data.decode("utf-8"))

        self.is_user(data)

    def test_get(self):
        self.test_add()

        r = self.app.post("/user/get", data={"email": self.user['email']})
        data = json.loads(r.data.decode("utf-8"))

        self.is_user(data)

    def test_delete(self):
        self.test_add()

        r = self.app.post("/user/delete", data={"email": self.user['email']})
        data = json.loads(r.data.decode("utf-8"))

        self.is_user(data)

        r = self.app.post("/user/get", data={"email": self.user['email']})
        data = json.loads(r.data.decode("utf-8"))

        self.assertTrue('status' in data)
        self.assertEqual(data['message'], "Could not find user")

    def tearDown(self):
        os.close(self.db)
        os.unlink(server.app.config['DATABASE'])

if __name__ == "__main__":
    unittest.main()
