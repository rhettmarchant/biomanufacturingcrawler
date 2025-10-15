import src.biomfg_crawler.query as query
import src.biomfg_crawler.crawl as crawl
import src.biomfg_crawler.download as download
from dotenv import load_dotenv
import os
import json

load_dotenv()

api_key = os.getenv("GOOGLE_CUSTOM_SEARCH_API_KEY")
cx = os.getenv("GOOGLE_CUSTOM_SEARCH_ENGINE_CX")

chemical = {
    'name': 'polylactic_acid',
    'synonyms': ['polylactide', 'poly(lactic) acid']
}

keywords = {
    'method': ['biomanufacturing', 'bioreactor', 'fermentation'],
    'volume': ['ton', 'tons', 'tonnes', 'metric ton'],
    'production': ['production capacity', 'annual production', 'annual capacity'],
    'feedstock': ['corn', 'sugar', 'sugarcane', 'biomass', 'starch', 'glucose']
}

chemical_query = query.generate_chemical_query(chemical['name'], chemical['synonyms'])
search_terms = query.generate_search_terms(keywords)
google_query = query.generate_google_query(chemical_query, search_terms)
response = crawl.google_search(api_key, cx, google_query, start=11)
links = crawl.extract_links(response)
json.dump(response, open("docs/output/example_links.json", "w"), indent=2)

results = []
blacklist = set()
whitelist = set()
for link in links:
    result = download.download(link, whitelist, blacklist, post_sleep=10, whitelist_sleep=30, force=False)
    results.append(result)
json.dump(results, open("docs/output/example_links_scraped.json", "w"), indent=2)
results = json.load(open("docs/output/example_links_scraped.json"))

for result in results:
    download.submit_to_ai(result, "docs/patterns.txt", "english", post_sleep=60)
json.dump(results, open("docs/output/example_links_ai_output.json", "w"), indent=2)
