import requests
from fastapi import FastAPI, Request
from auth import updated_token

app = FastAPI()

async def parse_csv_body(request: Request) -> list:
    """
    Takes a Request object and return list of vehicle in format of dictionary
    """
    csv = await request.body()
    csv = csv.decode("utf-8")
    rows = csv.split("\n")
    keys = rows[0].split(",")
    vehicles = [dict(zip(keys, row.split(","))) for row in rows[1:] if row]
    return vehicles

def fetch_additional_resources(vehicles: list) -> list:
    """
    Fetch additional resources from external API and merge it with the vehicles list
    """
    api_url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
    headers = {"Authorization": f"Bearer {updated_token}"}
    api_response = requests.get(api_url, headers=headers).json()
    vehicles += api_response
    return vehicles

def filter_by_hu(vehicles: list) -> list:
    """
    Filters the vehicles based on the "hu" field
    """
    vehicles = [vehicle for vehicle in vehicles if "hu" in vehicle]
    return vehicles

def resolve_label_ids(vehicles: list) -> list:
    """
    Resolves the labelIds and add colorCode field to the vehicles
    """
    if any("labelId" in vehicle for vehicle in vehicles):
        label_url = "https://api.baubuddy.de/dev/index.php/v1/labels/{vehicle}"
        for vehicle in vehicles:
            if "labelIds" in vehicle:
                vehicle["colorCode"] = requests.get(label_url.format(vehicle["labelIds"])).json()
    return vehicles

@app.post("/vehicles")
async def merge_vehicles(request: Request) -> list:
    """
    This function call all above functions in order 
    """
    vehicles = await parse_csv_body(request)
    vehicles = fetch_additional_resources(vehicles)
    vehicles = filter_by_hu(vehicles)
    vehicles = resolve_label_ids(vehicles)
    return vehicles
