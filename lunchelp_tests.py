#!/usr/bin/env python3

import server

import json
import os
import tempfile
import unittest

class TestUser(unittest.TestCase):

    def setUp(self):
        self.app = server.app.test_client()
        self.db, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.config['TESTING'] = True
        self.user = {"email": "testing@bendoan.me",
                "name": "Ben doan",
                "password": "password"}

    def is_user(self, data):
        self.assertTrue('email' in data)
        self.assertEqual(self.user['email'], data['email'])

        self.assertTrue('name' in data)
        self.assertEqual(self.user['name'], data['name'])

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

class TestGroup(unittest.TestCase):

    def is_group(self, data):
        self.assertTrue('name' in data)
        self.assertEqual(self.group['name'], data['name'])

    def setUp(self):
        self.app = server.app.test_client()
        self.db, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.config['TESTING'] = True
        self.group = {'name': 'RACE Team'}

    def test_add(self):
        r = self.app.post("/group/add", data=self.group)
        data = json.loads(r.data.decode("utf-8"))

        self.is_group(data)

    def test_get(self):
        self.test_add()

        r = self.app.post("/group/get", data=self.group)
        data = json.loads(r.data.decode("utf-8"))

        self.is_group(data)

    def test_delete(self):
        self.test_add()

        r = self.app.post("/group/delete", data=self.group)
        data = json.loads(r.data.decode("utf-8"))

        self.is_group(data)

        r = self.app.post("/group/get", data=self.group)
        data = json.loads(r.data.decode("utf-8"))

        self.assertTrue('status' in data)
        self.assertEqual(data['message'], "Could not find group")

    def tearDown(self):
        os.close(self.db)
        os.unlink(server.app.config['DATABASE'])

class TestGroup(unittest.TestCase):

    def is_resturant(self, data):
        self.assertTrue('name' in data)
        self.assertEqual(self.resturant['name'], data['name'])

    def setUp(self):
        self.app = server.app.test_client()
        self.db, server.app.config['DATABASE'] = tempfile.mkstemp()
        server.app.config['TESTING'] = True
        self.resturant = {'name': 'Sakura Bana', 'address': "7425 W Dodge Rd, Omaha, NE."}

    def test_add(self):
        r = self.app.post("/resturant/add", data=self.resturant)
        data = json.loads(r.data.decode("utf-8"))

        self.is_resturant(data)

    def test_get(self):
        self.test_add()

        r = self.app.post("/resturant/get", data={"name": self.resturant['name']})
        data = json.loads(r.data.decode("utf-8"))

        self.is_resturant(data)

    def test_delete(self):
        self.test_add()

        r = self.app.post("/resturant/delete", data={"name": self.resturant['name']})
        data = json.loads(r.data.decode("utf-8"))

        self.is_resturant(data)

        r = self.app.post("/resturant/get", data={"name": self.resturant['name']})
        data = json.loads(r.data.decode("utf-8"))

        self.assertTrue('status' in data)
        self.assertEqual(data['message'], "Could not find resturant")

    def tearDown(self):
        os.close(self.db)
        os.unlink(server.app.config['DATABASE'])

if __name__ == "__main__":
    unittest.main()
