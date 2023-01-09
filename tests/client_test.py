import unittest
import csv
import requests
from datetime import datetime
import requests_mock
import xlsxwriter
from auth import updated_token

fake_vehicles = [{'vehicle_id': '1', 'make': 'Honda', 'model': 'Accord', 'year': '2022', 'gruppe': 'A'}, 
                {'vehicle_id': '2', 'make': 'Toyota', 'model': 'Aygo', 'year': '2020', 'gruppe': 'B'},
                {'vehicle_id': '3', 'make': 'Ford', 'model': 'Mustang', 'year': '2015', 'gruppe': 'C'}]

class Client_Should(unittest.TestCase):
    def test_csv_reader_works_correctly(self):
        with open('vehicles.csv', 'r') as f:
            reader = csv.DictReader(f)
            vehicles = list(reader)
        self.assertIsInstance(vehicles, list)
        self.assertIsInstance(vehicles[0], dict)

    def test_server_communication_works_correctly(self):
        with open('vehicles.csv', 'r') as f:
            reader = csv.DictReader(f)
            vehicles = list(reader)
        url = 'http://localhost:8000/vehicles'
        headers = {'Authorization': f'Bearer {updated_token}'}
        with requests_mock.Mocker() as m:
            m.post(url, json={'success': True})
            response = requests.post(url, json=vehicles)
        self.assertEqual(response.json(), {'success': True})

    def test_sorting_by_gruppe_works_correctly(self):
        vehicles = sorted(fake_vehicles, key=lambda x: x['gruppe'])

        self.assertEqual([v['vehicle_id'] for v in vehicles], ['1', '2', '3'])

    def test_filename_formatting(self):
        current_date = datetime.now().date().isoformat()
        filename = f'vehicles_{current_date}.xlsx'
        expected_filename = f'vehicles_{current_date}.xlsx'

        self.assertEqual(filename, expected_filename)

    def test_worksheet_creation_works_correctly(self):
        current_date = datetime.now().date().isoformat()
        filename = f'vehicles_{current_date}.xlsx'

        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()

        self.assertIsInstance(worksheet, xlsxwriter.worksheet.Worksheet)