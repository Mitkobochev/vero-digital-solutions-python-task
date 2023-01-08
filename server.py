import requests
from fastapi import FastAPI, Request
from auth import updated_token

app = FastAPI()

@app.post("/vehicles")
async def merge_vehicles(request: Request) -> list:
    # Retrieve request body as CSV
    csv = await request.body()
    csv = csv.decode("utf-8")
    rows = csv.split("\n")
    keys = rows[0].split(",")
    vehicles = [dict(zip(keys, row.split(","))) for row in rows[1:] if row]
    
    # Request additional resources and merge with request body
    api_url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
    headers = {"Authorization": f"Bearer {updated_token}"}
    api_response = requests.get(api_url, headers=headers).json()
    vehicles += api_response
    
    # Filter by HU field
    vehicles = [vehicle for vehicle in vehicles if "hu" in vehicle]

    # Resolve labelIds and add colorCode field
    if any("labelId" in vehicle for vehicle in vehicles):
        label_url = "https://api.baubuddy.de/dev/index.php/v1/labels/{vehicle}"
        for vehicle in vehicles:
            if "labelIds" in vehicle:
                vehicle["colorCode"] = requests.get(label_url.format(vehicle["labelIds"])).json()
                return vehicle

    return vehicles