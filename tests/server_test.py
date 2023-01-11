import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from auth import updated_token
from server import app, parse_csv_body, fetch_additional_resources, filter_by_hu

FAKE_VEHICLES = [{'id': 1, 'name': 'Vehicle 1', 'gruppe': 'Group A', 'hu': '2022-01-01'},
                 {'id': 2, 'name': 'Vehicle 2', 'gruppe': 'Group B'}]

client = TestClient(app)

class Server_Should(unittest.TestCase):
    async def test_parse_csv_body_works_correctly(self):
        csv = 'id,name,gruppe\n1,Vehicle 1,Group A\n'
        with patch('server.parse_csv_body', return_value=csv):
            vehicles = await parse_csv_body(app)
            self.assertEqual(vehicles[0]['name'], 'Vehicle 1')

    @patch('requests.get')
    def test_fetch_additional_resources_works_correctly(self, mock_get):
        additional_vehicles = [
            {'id': 3, 'name': 'Vehicle 3', 'gruppe': 'Group C'}]
        mock_get.return_value.json.return_value = additional_vehicles
        updated_vehicles = fetch_additional_resources(FAKE_VEHICLES)
        self.assertEqual(updated_vehicles[-1]['name'], 'Vehicle 3')

    def test_filter_by_hu_works_correctly(self):
        filtered_vehicles = filter_by_hu(FAKE_VEHICLES)

        self.assertEqual(len(filtered_vehicles), 1)

    def test_merge_vehicles_returns_correct_output(self):
        csv = "rnr,hu,kurzname,info\n123,2022-01-28T07:43:26Z,Vehicle 1,Information 1"
        response = client.post("/vehicles", data=csv)
        data = response.json()
        result = data[0]

        self.assertEqual(
            result, {'rnr': '123', 'hu': '2022-01-28T07:43:26Z', 'kurzname': 'Vehicle 1', 'info': 'Information 1'})