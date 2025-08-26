from dotenv import load_dotenv
import requests
import json
import os

## 26 August 2025 - 2:30pm
# For next time:
# Extract URLs and pass into OPENAI
# Establish new test database for BCMV
# Handle batch input for URL to OPENAI
# Bulk import data to test database
# Sort out pagination problem
# Repeat with full dataset.

## Cheap win
# 1. Create a spreadsheet with all of the chemicals of interest
# 2. Work out how much relevant data is out there and create a table

load_dotenv()

API_KEY = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
CX = os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_CX")

print("API_KEY: ", API_KEY)
print("CX: ", CX)

def google_search(query, exact, sort):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "exactTerms": exact,
        "sort": sort
    }
    resp = requests.get(url, params=params)
    if resp.status_code == 403:
        raise Exception("[403] Access forbidden: Check your API key, CX, or quota.")
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    query = '("polylactic acid" OR polylactide) (biomanufacturing OR bioreactor OR fermentation) ("ton" OR "tons" OR "tonnes" OR "metric ton" OR "metric tons" OR "metric tonnes") -simulation'
    exact = "production capacity"
    sort = "date:r:20250701:"
    print("QUERY: ", query)
    print("EXACT TERMS: ", exact)
    print("SORT: ", sort)
    results = google_search(query, exact, sort)
    print(json.dumps(results, indent=2))
