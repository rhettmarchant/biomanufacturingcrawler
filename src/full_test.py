import src.query_generation as qg
import src.search_api as sa
import src.ai_api_integration as aiapi
import json

if __name__ == "__main__":
    chemicals_tsv = 'August 2025 - GyG AI Screening Terms - Chemicals.tsv'
    queries_tsv = 'August 2025 - GyG AI Screening Terms - Queries.tsv'

    chemicals = qg.import_chemical_names(chemicals_tsv)
    search_terms = qg.import_search_terms_tsv(queries_tsv)

    en_searches = qg.generate_search_query(chemicals, search_terms, 'english')
    qg.export_to_tsv(en_searches, 'August 2025 - GyG AI Queries - English.tsv')

    zh_searches = qg.generate_search_query(chemicals, search_terms, 'chinese')
    qg.export_to_tsv(zh_searches, 'August 2025 - GyG AI Queries - Chinese.tsv')

    query = en_searches['polylactic acid']
    results = sa.google_search(query, "date:r")
    product = sa.extract_results(results)
    links = sa.extract_links(product)
    results = aiapi.bulk_ai_search(links)

    print(json.dumps(product['search'], indent=2))
    print(json.dumps(results, indent=2))

