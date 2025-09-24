# query_chemicals
# name_en:
# synonyms_en:
# abbreviations_en:
# name_zh:
# synonyms_zh:

# search_term
# term:
# category: methods, volumes, production, or feedstock
# language: english, chinese
chemical_query = "1,10-diaminodecane"

keywords = {
    'Method': ['biomanufacturing', 'bioreactor', 'fermentation'],
    'Volume': ['ton', 'tons', 'tonnes', 'metric ton', 'metric tons', 'metric tonnes', 'litres'],
    'Production': ['production capacity', 'annual production', 'annual capacity'],
    'Feedstock': ['corn', 'sugar', 'sugarcane', 'biomass', 'starch', 'glucose']
}

search_terms = ['(biomanufacturing OR bioreactor OR fermentation)',
                '(ton OR tons OR tonnes OR "metric ton" OR "metric tons" OR "metric tonnes" OR litres)',
                '("production capacity" OR "annual production" OR "annual capacity")',
                '(corn OR sugar OR sugarcane OR biomass OR starch OR glucose)']

def generate_search_terms(keywords):
    search_terms = []
    for category, terms in keywords.items():
        search_terms.append(f"({' OR '.join([f'\"{term}\"' for term in terms])})")
    return search_terms

def generate_google_query(chemical_query, search_terms):
    search_query = " AND ".join(search_terms)
    return f"{chemical_query} AND {search_query}"

generate_google_query(chemical_query, search_terms)
generate_google_query(chemical_query, generate_search_terms(keywords))