import requests

def google_search(api_key, cx, query, start = 1,):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "start": start
    }
    resp = requests.get(url, params=params)
    if resp.status_code == 403:
        raise Exception(
            "[403] Access forbidden: Check your API key, CX, or quota.")
    resp.raise_for_status()
    return resp.json()

def extract_links(google_search):
    links = [item.get("link") for item in google_search.get("items", [])]
    return links