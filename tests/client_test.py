import unittest
from unittest.mock import Mock, patch
import client
import csv

fake_vehicles = [{'vehicle_id': '1', 'make': 'Honda', 'model': 'Accord', 'year': '2022', 'gruppe': 'A'},
                 {'vehicle_id': '2', 'make': 'Toyota',
                     'model': 'Aygo', 'year': '2020', 'gruppe': 'B'},
                 {'vehicle_id': '3', 'make': 'Ford', 'model': 'Mustang', 'year': '2015', 'gruppe': 'C'}]


class Client_Should(unittest.TestCase):
    
    def test_csv_reader_works_correctly(self):
        with open('vehicles.csv', 'r') as f:
            reader = csv.DictReader(f)
            vehicles = list(reader)
        self.assertIsInstance(vehicles, list)
        self.assertIsInstance(vehicles[0], dict)

    @patch('requests.post')
    def test_transmit_csv_works_correctly(self, mock_post):
        vehicles = [{'rnr': '123', 'kurzname': 'Vehicle 1'}]
        headers = {'Authorization': 'Bearer token'}
        mock_response = Mock()
        mock_response.json.return_value = {'status': 'success'}
        mock_post.return_value = mock_response

        result = client.transmit_csv(vehicles, headers)

        mock_post.assert_called_once_with(
            'http://localhost:8000/vehicles', json=vehicles, headers=headers)
        mock_response.json.assert_called_once()
        self.assertEqual(result, {'status': 'success'})

    def test_sort_vehicles_works_correctly(self):
        sorted_vehicles = client.sort_vehicles(fake_vehicles)

        self.assertEqual(sorted_vehicles[0]['gruppe'], 'A')
        self.assertEqual(sorted_vehicles[1]['gruppe'], 'B')
        self.assertEqual(sorted_vehicles[2]['gruppe'], 'C')

    def test_add_headers_works_correctly(self):
        headers = [{'rnr': '123', 'kurzname': 'Vehicle 1'}]

        mock_worksheet = Mock()
        client.add_headers(mock_worksheet, headers)

        mock_worksheet.write_row.assert_called_once_with(
            0, 0, list(headers[0].keys()))
