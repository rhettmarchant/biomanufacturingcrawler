from dotenv import load_dotenv
import requests
import json
import os
from biomanufacturingtracker.src.extractors.sourceExtract import extract_source

load_dotenv()

API_KEY = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
CX = os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_CX")

user_prompt = "biomanufacturingtracker/src/ai_prompts/userPrompt.txt"
system_prompt = "biomanufacturingtracker/src/ai_prompts/prompt_getRecords.md"

print("API_KEY: ", API_KEY)
print("CX: ", CX)


def google_search(query, sort):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": query,
        "sort": sort,
        # Note, the API will never return more than 10 pages of results (i.e. 101)
        "start": 91
    }
    resp = requests.get(url, params=params)
    if resp.status_code == 403:
        raise Exception(
            "[403] Access forbidden: Check your API key, CX, or quota.")
    resp.raise_for_status()
    return resp.json()


def extract_results(json_data):
    items = []
    search = {
        "totalResults": json_data['queries']['request'][0]['totalResults'],
        "searchTerms": json_data['queries']['request'][0]['searchTerms'],
        "count": json_data['queries']['request'][0]['count'],
        "startIndex": json_data['queries']['request'][0]['startIndex']
    }
    if "items" in json_data:
        for item in json_data["items"]:
            result = {
                "title": item["title"],
                "link": item["link"],
                "snippet": item["snippet"],
                "json": item
            }
            items.append(result)
    product = {'search': search, 'items': items}
    return product


def extract_links(product):
    links = [item['link'] for item in product['items']]
    return links


def bulk_ai_search(links):
    results = []
    for url in links:
        json = extract_source(url, system_prompt, user_prompt)
        results.append(json)
    return results



if __name__ == "__main__":
    query = '("polylactic acid" OR polylactide) (biomanufacturing OR bioreactor OR fermentation) ("ton" OR "tons" OR "tonnes" OR "metric ton" OR "metric tons" OR "metric tonnes") -simulation'
    sort = "date:r"
    print("QUERY: ", query)
    print("SORT: ", sort)
    results = google_search(query, sort)
    product = extract_results(results)
    links = extract_links(product)
    results = bulk_ai_search(links)
    print(json.dumps(product['search'], indent=2))
    #print(json.dumps(links, indent=2))
    print(json.dumps(results, indent=2))
