import unittest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


class TestServer(unittest.TestCase):
    def test_merge_vehicles_returns_correct_status_code(self):
        csv = "rnr,hu,kurzname,info\n123,2022-01-28T07:43:26Z,Vehicle 1,Information 1"
        response = client.post("/vehicles", data=csv)

        self.assertEqual(response.status_code, 200)

    def test_merge_vehicles_returns_correct_output(self):
        csv = "rnr,hu,kurzname,info\n123,2022-01-28T07:43:26Z,Vehicle 1,Information 1"
        response = client.post("/vehicles", data=csv)
        data = response.json()
        result = data[0]

        self.assertEqual(
            result, {'rnr': '123', 'hu': '2022-01-28T07:43:26Z', 'kurzname': 'Vehicle 1', 'info': 'Information 1'})
