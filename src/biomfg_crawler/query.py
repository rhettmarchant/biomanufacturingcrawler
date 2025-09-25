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

def generate_chemical_query(name, synonyms = None, abbreviations = None):
    if name and not synonyms and not abbreviations:
        return name
    
    if name and (synonyms or abbreviations):
        terms = [name]
        if synonyms:
            terms.extend(synonyms)
        if abbreviations:
            terms.extend(abbreviations)
        return f"({' OR '.join([f'\"{term}\"' for term in terms])})"
    
    if name and synonyms and abbreviations:
        terms = [name] + synonyms + abbreviations
        return f"({' OR '.join([f'\"{term}\"' for term in terms])})"

def generate_search_terms(keywords):
    search_terms = []
    for category, terms in keywords.items():
        search_terms.append(f"({' OR '.join([f'\"{term}\"' for term in terms])})")
    return search_terms

def generate_google_query(chemical_query, search_terms):
    if len(search_terms) == 0:
        return chemical_query
    else:
        search_query = " AND ".join(search_terms)
    return f"{chemical_query} AND {search_query}"