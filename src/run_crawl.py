import src.query_generation as qg
import src.search_api as sa
import src.ai_api_integration as aiapi
import json

# INPUT: List of chemicals + A new query + List of links already searched
# OUTPUT: AI Extracted Results in JSON + Updated list of links already searched + Query progress metrics

# MODELS: Query is the top level. Each query has multiple chemicals, each chemical has multiple searches
#
# QUERY: name, pattern, language, chemicals
# QCHEMICAL: name, searches
# QSEARCH: chemical, query, search_string, total_results, completed_results, links
#
# Query: name: "Place x Method x Feedstock x Capacity x Volume"
#        pattern: "1,10-diaminodecane AND (biomanufacturing OR bioreactor OR fermentation) AND (corn OR sugar OR sugarcane OR biomass OR starch OR glucose) AND (production capacity OR annual production OR annual capacity) AND (ton OR tons OR tonnes OR metric ton OR metric tons OR metric tonnes OR litres)"
#        language: "english"
#        chemicals: ["1,10-diaminodecane", "2,5-furandicarboxylic acid", "3-hydroxypropionic acid", "5-aminovalanoicacid"]
#
# QChemical: name: "1,10-diaminodecane"
#            searches: ... (see below)
#
# QSearch: chemical: "1,10-diaminodecane"
#         query: "Place x Method x Feedstock x Capacity x Volume"
#         search_string:"1,10-diaminodecane AND (biomanufacturing OR bioreactor OR fermentation) AND (corn OR sugar OR sugarcane OR biomass OR starch OR glucose) AND (production capacity OR annual production OR annual capacity) AND (ton OR tons OR tonnes OR metric ton OR metric tons OR metric tonnes OR litres)"
#         total_results: 17336
#         available_results: 100
#         available_pages: 10
#         completed_pages: 1
#         completed_results: 10
#         links: [https://example.com/search1, https://example.com/search2, ...]

# 1. Building Queries (ensure there is a query for each chemical in each language)
def build_queries(chemicals_tsv, queries_tsv):
    # How often are we doing this? Only when a new query set needs to be built
    # Chemicals might actually be stored in the database itself
    chemicals = qg.import_chemical_names(chemicals_tsv)
    search_terms = qg.import_search_terms_tsv(queries_tsv)
     
    en_searches = qg.generate_search_query(chemicals, search_terms, 'english')
    zh_searches = qg.generate_search_query(chemicals, search_terms, 'chinese')
     
    return {"english": en_searches, "chinese": zh_searches}

# 2. Pilot Search (to determine how many results are available for each chemical in each language)
def pilot_search():
    # This will be done at the first initialisation of each query
    # This could be a simple addition to the first search (i.e. pilot search done or nah?)
    return


# 3. Search Calculations (determine the number of paged API called to be made per chemical-query)
        # Query 1: Feedstock mentioned (primary bias)
        # $Chemical AND $Method AND $Volume AND $Capacity AND $Feedstock
            # Method:"biomanufacturing" OR "bioreactor" OR "fermentation"
            # Volume: "ton" OR "tons" OR "tonnes" OR "metric ton" OR "metric tons" OR "metric tonnes" OR "litres"
            # Capacity: "production capactiy" OR "annual production" OR "annual capacity"
            # Feedstock: "corn" OR "sugar" OR "sugarcane" OR "biomass" OR "starch" OR "glucose"
        # 0/3   1,10-diaminodecane OR decamethylenediamine
        # 0/10  2,5-furandicarboxylic acid
        # 0/10  3-hydroxypropionic acid
        # 0/0   5-aminovalanoicacid

def search_calculation(search_results_file, output_tsv=None):
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


# 4. Run search across all chemicals, stopping once the limit for the chemical-query pair is reached
def google_by_chemical(queries, language, tracker = None, search_index=1, query_limit=56):
    # Will need code that checks how many searches have already been done for each chemical-query pair and whether the limit has been reached
    # Firstly check that the pilot search has been done, if not, perform all searches.
    # If it has been done, check how many searches have been done and only perform the remaining searches
    # search_index = 1 for first 10 results, 11 for second 10, 21 for third 10, etc.
    if tracker:
        search_chemicals = [f"{key}" for key, value in queries[language].items()]
        query_chemicals = []
        for chemical in search_chemicals:
            if chemical in tracker:
                if search_index // 10 + (1 if search_index % 10 > 0 else 0) > tracker[chemical]['total_searches']:
                    print(f"Skipping {chemical}, already completed {tracker[chemical]['completed_searches']} of {tracker[chemical]['total_searches']} searches")
                    continue
                else:
                    query_chemicals.append(chemical)
        
        search_chemicals = query_chemicals
     
    else:
        search_chemicals = [f"{key}" for key, value in queries[language].items()]
    
    google_results_by_chemical = {}
    
    for chemical in search_chemicals[:query_limit]:
        data = sa.google_search(queries[language][chemical], "date:r", search_index)
        google_results_by_chemical[chemical] = sa.extract_results(data)
     
    if tracker:
        for chemical in google_results_by_chemical:
            if chemical in tracker:
                tracker[chemical]['completed_searches'] += 1
    else:
        tracker = search_calculation(google_results_by_chemical)
     
    return {"search_results": google_results_by_chemical, "tracker": tracker}


def search_calculation(search_results):
    chemical_totals = {}
    for chemical, product in search_results.items():
        total_results = int(product['search']['totalResults'])
        total_searches = total_results // 10 + (1 if total_results % 10 > 0 else 0)
        total_searches = min(total_searches, 10)
        chemical_totals[chemical] = { "total_results": total_results, "completed_searches": 1, "total_searches": total_searches }
     
    return chemical_totals


# 5. Extract the links from the search results
def extract_links_from_json(search_results):
    link_list = []
    for chemical, result in search_results.items():
        links = sa.extract_links(result)
        link_list.extend(links)
    return link_list


# 6. De-duplicate links, select unique, and aggregate with all previously extracted links
def extract_unique_links(all_unique_link_file, search_results):
    with open(all_unique_link_file) as f:
        unique_links = json.load(f)
     
    links = extract_links_from_json(search_results)
     
    combined_links = set(unique_links + links)
    with open(all_unique_link_file, 'w') as f:
        json.dump(list(combined_links), f, indent=2)
    
    unique_subset = set(links).difference(set(unique_links))
    new_link_pct = len(unique_subset) / len(links) * 100
    
    print(f"{len(combined_links)} total unique links, {len(unique_subset)} ({new_link_pct}%) new links")
     
    return list(unique_subset)


# 7. Perform AI data extraction on the de-duplicated links and store as JSON
# aiapi.bulk_ai_search(links)


# 8. Aggregate and clean AI results
def clean_ai_json(ai_data):
    filtered_data = [entry for entry in ai_data if entry.get('company_1')]
     
    return filtered_data


# 9. Bulk upload sources and AI results to database


# Example Workflow
# ----------------
queries = build_queries(chemicals_tsv='reference/August 2025 - GyG AI Screening Terms - Chemicals.tsv',
              queries_tsv='reference/August 2025 - GyG AI Screening Terms - Queries.tsv')
search_results = google_by_chemical(queries, 'english', search_index=1, query_limit=2)
tracker = search_results['tracker']
unique_links = extract_unique_links('output/test.json', search_results)
ai_data = aiapi.bulk_ai_search(unique_links)
clean_ai_data = clean_ai_json(ai_data)