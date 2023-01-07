import argparse
import requests
import csv
import xlsxwriter
import dateutil.parser
from datetime import datetime
from auth import updated_token

# Parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('-k', '--keys', nargs='+', required=True)
parser.add_argument('-c', '--colored', action='store_true', default=True)
args = parser.parse_args()

# Read CSV file
with open('vehicles.csv', 'r') as f:
    reader = csv.DictReader(f)
    vehicles = list(reader)

# Transmit CSV to server and retrieve response
url = 'http://localhost:8000/vehicles'
headers = {'Authorization': f'Bearer {updated_token}'}
response = requests.post(url, json=vehicles)
vehicles = response.json()

# Sort vehicles by gruppe
vehicles = sorted(vehicles, key=lambda x: x['gruppe'])
for vehicle in vehicles:
    for key in args.keys:
        if key in vehicle:
            vehicle[key] = vehicle[key]

# Save to Excel file
current_date = datetime.now().date().isoformat()
filename = f'vehicles_{current_date}.xlsx'
workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet()

# Add header
headers = list(vehicles[0].keys())
worksheet.write_row(0, 0, headers)

# Color cells based on ColorCode
red_format = workbook.add_format({'color': '#b30000'})
orange_format = workbook.add_format({'color': '#FFA500'})
green_format = workbook.add_format({'color': '#007500'})

for i, row in enumerate(vehicles, start=1):
    for j, key in enumerate(row):
        if args.colored and key == 'hu' and row[key] is not None:
                # Set cell's text color based on HU
                hu_date = dateutil.parser.parse(row[key])
                hu_age_in_months = (datetime.now() - hu_date).days / 30
                if hu_age_in_months <= 3:
                    worksheet.write(i, j, row[key], green_format)
                elif hu_age_in_months <= 12:
                    worksheet.write(i, j, row[key], orange_format)
                else:
                    worksheet.write(i, j, row[key], red_format)
        else:
            worksheet.write(i, j, row[key])


workbook.close()
print(f'Saved as {filename}')