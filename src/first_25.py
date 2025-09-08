import src.query_generation as qg
import src.search_api as sa
import src.ai_api_integration as aiapi
import json

# I want to extract out the data for the first page for the first 25 chemicals
# That means using the first 25 search queries with a startIndex of 1
# I need a way to store the returning json and the extracted links.

if __name__ == "__main__":
    # So 1, generate the queries
    chemicals_tsv = 'reference/August 2025 - GyG AI Screening Terms - Chemicals.tsv'
    queries_tsv = 'reference/August 2025 - GyG AI Screening Terms - Queries.tsv'

    chemicals = qg.import_chemical_names(chemicals_tsv)
    search_terms = qg.import_search_terms_tsv(queries_tsv)

    en_searches = qg.generate_search_query(chemicals, search_terms, 'english')
    qg.export_to_tsv(en_searches, 'reference/August 2025 - GyG AI Queries - English.tsv')

    zh_searches = qg.generate_search_query(chemicals, search_terms, 'chinese')
    qg.export_to_tsv(zh_searches, 'reference/August 2025 - GyG AI Queries - Chinese.tsv')

    #Then 2, get the chemical keys
    chemicals = [f"{key}" for key, value in en_searches.items()]

    #Then 3, iterate over the keys to perform the search
    bulk_products = {}

    for chemical in chemicals[:56]:
        data = sa.google_search(en_searches[chemical], "date:r", 21)
        bulk_products[chemical] = sa.extract_results(data)

        #links = sa.extract_links(bulk_products[chemical])
        #bulk_results[chemical] = aiapi.bulk_ai_search(links)

    #And 4, store the product, links, and results in json format
    with open('output/google_output.json', 'w') as f:
        json.dump(bulk_products, f, indent=2)

    #And 5, extract the links
    #read in the JSON
    with open('output/chinese/August_2025_GyG_Google_API_Search_Results_Chinese_pg2.json', 'r') as f:
        bulk_products = json.load(f)

    link_list = []
    for chemical, links in bulk_products.items():
        link_list.extend(sa.extract_links(bulk_products[chemical]))

    with open('output/link_list.json', 'w') as f:
        json.dump(link_list, f, indent=2)

    with open('output/link_diff_eng_all_pg3.json', 'r') as f:
        link_list = json.load(f)

    unique_links = list(set(link_list)) # There are 266 unique links in this dataset

    bulk_ai_responses_1_236 = aiapi.bulk_ai_search(unique_links[1:])
    bulk_ai_responses_100_200 = aiapi.bulk_ai_search(unique_links[100:200])
    bulk_ai_responses_200_300 = aiapi.bulk_ai_search(unique_links[200:])
    #bulk_ai_responses_300_388 = aiapi.bulk_ai_search(unique_links[300:])

    with open('output/ai_en_output_1_236.json', 'w') as f:
        json.dump(bulk_ai_responses_1_236, f, indent=2)
    with open('output/ai_en_output_100_200.json', 'w') as f:
        json.dump(bulk_ai_responses_100_200, f, indent=2)
    with open('output/ai_en_output_200_302.json', 'w') as f:
        json.dump(bulk_ai_responses_200_300, f, indent=2)
    with open('output/ai_en_output_300_388.json', 'w') as f:
        json.dump(bulk_ai_responses_300_388, f, indent=2)


    # Find links in en_searches 53:56 not in 1:53
    with open('output/english/August_2025_GyG_Google_API_Links_English_pg1.json') as f:
        links_pg1 = json.load(f)

    with open('output/english/August_2025_GyG_Google_API_Links_All_Unique_English.json') as f:
        links_pg2 = json.load(f)

    combined_links = set(links_pg1 + links_pg2)
    with open('output/all_english_links.json', 'w') as f:
        json.dump(list(combined_links), f, indent=2)

    diff1 = set(links_pg2).difference(set(links_pg1))
    with open('output/link_diff_eng_next_batch.json', 'w') as f:
        json.dump(list(diff1), f, indent=2)

    bulk_ai_responses_diff1 = aiapi.bulk_ai_search(list(diff1))
    with open('output/ai_output_diff1.json', 'w') as f:
        json.dump(bulk_ai_responses_diff1, f, indent=2)


# Identify new links to pass to AI, don't double up on links already passed
# Only make API calls that are going to be useful i.e. don't do a google search
# if we know there aren't enough results to be returned.

# We have 56 target chemicals
# We have two branches: chinese and english

# We want to use the same search terms until they are exhausted.

# We want to pull out up to the first 100 links per chemical search query

# We want to extract the links from the google search results, de-duplicate them
# and then pass them to the AI API.

# Here's the general workflow
# 1. Generate the search queries for both languages
# 2. For each chemical in each language, perform a google search with the query
    # Check the total results returned and ensure no additional searches.
    # Need a way to keep track (pilot search)
# 3. Extract the links from the search results
# 4. De-duplicate the links
# 5. Pass the unique links to the AI API
# 6. Store the results in a JSON file


import csv

def google_by_chemical(queries_file, output_file, search_index=1, query_limit=56):
    with open(queries_file, 'r', encoding='utf-8') as prebuilt_queries:
        query_table = csv.reader(prebuilt_queries, delimiter='\t')
        en_searches = {row[0]: row[1] for row in query_table if len(row) >= 2}
    search_chemicals = [f"{key}" for key, value in en_searches.items()]
    google_results_by_chemical = {}
    for chemical in search_chemicals[:query_limit]:
        data = sa.google_search(en_searches[chemical], "date:r", search_index)
        google_results_by_chemical[chemical] = sa.extract_results(data)
    with open(output_file, 'w') as f:
        json.dump(google_results_by_chemical, f, indent=2)

google_by_chemical('reference/August 2025 - GyG AI Queries - English.tsv',
    'output/test.json',
    search_index=1,
    query_limit=2)

def extract_unique_links(all_unique_link_file, link_file, output_file_name):
    with open(all_unique_link_file) as f:
        unique_links = json.load(f)
     
    with open(link_file) as f:
        links = json.load(f)
     
    combined_links = set(unique_links + links)
    with open(all_unique_link_file, 'w') as f:
        json.dump(list(combined_links), f, indent=2)
     
    unique_subset = set(links).difference(set(unique_links))
    with open(output_file_name, 'w') as f:
        json.dump(list(unique_subset), f, indent=2)
     
    new_link_pct = len(unique_subset) / len(links) * 100
     
    return f"{len(combined_links)} total unique links, {len(unique_subset)} ({new_link_pct}%) new links"

extract_unique_links('output/chinese/August_2025_GyG_Google_API_Links_All_Unique_Chinese.json',
                     'output/chinese/August_2025_GyG_Google_API_Links_Chinese_pg2.json',
                     'output/link_diff_zh_next_batch.json')

# Organise by Query
# {Chemical} AND {Method} AND {Volume} AND {Capacity} AND {Feedstock}
# Create a table of chemicals and the total results returned

def chemical_totals_by_query(search_results_file, output_tsv=None):
    with open(search_results_file, 'r') as f:
        bulk_products = json.load(f)
    
    chemical_totals = {}
    for chemical, product in bulk_products.items():
        chemical_totals[chemical] = product['search']['totalResults']
    
    if output_tsv:
        with open(output_tsv, 'w') as f:
            for chemical, total in chemical_totals.items():
                f.write(f"{chemical}\t{total}\n")

    return chemical_totals

chemical_totals_by_query('output/english/August_2025_GyG_Google_API_Search_Results_English_pg1.json',
                         output_tsv='output/chemical_totals_en.tsv')

chemical_totals_by_query('output/chinese/August_2025_GyG_Google_API_Search_Results_Chinese_pg1.json',
                         output_tsv='output/chemical_totals_zh.tsv')


def clean_ai_json(file, output_file):
    with open(file, 'r') as f:
        data = json.load(f)
    filtered_data = [entry for entry in data if entry.get('company_1')]
     
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(filtered_data, f, indent=2)
     
    return filtered_data

clean_ai_json('August_2025_GyG_OpenAI_Results_English_pg1.json', 'clean_August_2025_GyG_OpenAI_Results_English_pg1.json')
clean_ai_json('August_2025_GyG_OpenAI_Results_English_pg2.json', 'clean_August_2025_GyG_OpenAI_Results_English_pg2.json')
clean_ai_json('August_2025_GyG_OpenAI_Results_English_pg3.json', 'clean_August_2025_GyG_OpenAI_Results_English_pg3.json')

clean_ai_json('August_2025_GyG_OpenAI_Results_Chinese_pg1.json', 'clean_August_2025_GyG_OpenAI_Results_Chinese_pg1.json')
clean_ai_json('August_2025_GyG_OpenAI_Results_Chinese_pg2.json', 'clean_August_2025_GyG_OpenAI_Results_Chinese_pg2.json')