import argparse
import requests
import csv
import xlsxwriter
import dateutil.parser
from datetime import datetime
from auth import updated_token

def parse_args():
    """
    Taking the input parameters 
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keys', nargs='+', required=True)
    parser.add_argument('-c', '--colored', action='store_true', default=True)
    return parser.parse_args()

def read_csv(file):
    """
    Read csv file and returns list of dictionaries
    """
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def transmit_csv(vehicles, headers):
    """
    Transmit the vehicles to API
    """
    url = 'http://localhost:8000/vehicles'
    response = requests.post(url, json=vehicles, headers=headers)
    return response.json()

def sort_vehicles(vehicles):
    """
    Sort the vehicles by gruppe field
    """
    return sorted(vehicles, key=lambda x: x['gruppe'])

def color_cells(workbook,worksheet, vehicles, keys):
    """
    Add conditional formatting to excel cells
    """
    red_format = workbook.add_format({'color': '#b30000'})
    orange_format = workbook.add_format({'color': '#FFA500'})
    green_format = workbook.add_format({'color': '#007500'})

    for i, row in enumerate(vehicles, start=1):
        for j, key in enumerate(row):
            if keys and key == 'hu' and row[key] is not None:
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

def add_header(worksheet, vehicles):
    """
    Add headers to worksheet
    """
    headers = list(vehicles[0].keys())
    worksheet.write_row(0, 0, headers)

def save_to_excel(vehicles, colored, keys):
    """
    Save vehicles to excel
    """
    current_date = datetime.now().date().isoformat()
    filename = f'vehicles_{current_date}.xlsx'
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    add_header(worksheet, vehicles)
    color_cells(workbook,worksheet, vehicles, colored)

    workbook.close()
    print(f'Saved as {filename}')

def main():
    """
    This function call all above functions in order 
    """
    args = parse_args()
    data = read_csv('vehicles.csv')
    headers = {'Authorization': f'Bearer {updated_token}'}
    data = transmit_csv(data, headers)
    data = sort_vehicles(data)
    current_date = datetime.now().date().isoformat()
    filename = f'vehicles_{current_date}.xlsx'
    save_to_excel(data, filename, args.colored)

main()